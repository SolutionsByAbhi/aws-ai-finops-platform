 resource  "aws_s3_bucket"  "cost_data" {
     bucket =  "${var.prefix}-cost-data"
 }
 
resource  "aws_dynamodb_table"  "recommendations"  {
    name                = "${var.prefix}-recommendations"
     billing_mode =  "PAY_PER_REQUEST"
    hash_key         =  "id"
 
    attribute  {
       name  =  "id"
        type =  "S"
    }
 }
 
 resource "aws_iam_role"  "lambda_role"  {
    name                          =  "${var.prefix}-lambda-role"
    assume_role_policy  =  data.aws_iam_policy_document.lambda_assume.json
 }

 data  "aws_iam_policy_document"  "lambda_assume" {
     statement {
        actions  =  ["sts:AssumeRole"]
       principals  {
           type              =  "Service"
           identifiers  =  ["lambda.amazonaws.com"]
        }
    }
 }

 resource  "aws_iam_role_policy_attachment"  "lambda_basic" {
     role            =  aws_iam_role.lambda_role.name
    policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
 }
 
 resource "aws_lambda_function"  "ai_engine"  {
    function_name  =  "${var.prefix}-ai-engine"
    role                 =  aws_iam_role.lambda_role.arn
    handler             = "recommend_optimizations.lambda_handler"
     runtime            =  "python3.11"
    filename          =  "${path.module}/../../backend/ai-engine/bedrock/dist/ai_engine.zip"
 
    environment  {
        variables =  {
           RECOMMENDATION_TABLE  =  aws_dynamodb_table.recommendations.name
           AWS_REGION                   =  var.region
        }
    }
 }
 
resource  "aws_lambda_function"  "api"  {
    function_name  = "${var.prefix}-api"
     role                 =  aws_iam_role.lambda_role.arn
    handler            =  "handler.lambda_handler"
    runtime             = "python3.11"
     filename          =  "${path.module}/../../backend/api/lambda-api/dist/api.zip"
 
    environment  {
       variables  =  {
           RECOMMENDATION_TABLE  =  aws_dynamodb_table.recommendations.name
       }
     }
}
 
 resource  "aws_apigatewayv2_api" "http_api"  {
    name                  =  "${var.prefix}-finops-api"
    protocol_type  = "HTTP"
 }
 
 resource "aws_apigatewayv2_integration"  "lambda_integration"  {
    api_id                              =  aws_apigatewayv2_api.http_api.id
    integration_type            =  "AWS_PROXY"
    integration_uri              =  aws_lambda_function.api.arn
    payload_format_version  =  "2.0"
}
 
 resource  "aws_apigatewayv2_route" "costs"  {
    api_id       =  aws_apigatewayv2_api.http_api.id
    route_key  =  "GET  /costs"
    target       =  "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}
 
 resource  "aws_apigatewayv2_route" "recs"  {
    api_id       =  aws_apigatewayv2_api.http_api.id
    route_key  =  "GET  /recommendations"
    target       =  "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}
 
 resource  "aws_lambda_permission" "api_invoke"  {
    statement_id    =  "AllowAPIGatewayInvoke"
    action              =  "lambda:InvokeFunction"
    function_name  = aws_lambda_function.api.function_name
     principal        =  "apigateway.amazonaws.com"
    source_arn       =  "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
 }
