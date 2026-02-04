 import  os
 import json
 import  boto3
 from decimal  import  Decimal
 from datetime  import  datetime
 
dynamodb  =  boto3.resource("dynamodb")
 bedrock =  boto3.client("bedrock-runtime")
 
 TABLE_NAME =  os.environ["RECOMMENDATION_TABLE"]
 table  = dynamodb.Table(TABLE_NAME)
 
 PROMPT  = """
 You  are  a FinOps  expert.  Given  AWS service  cost  data  in JSON,  suggest  3–5  concrete optimization  actions.
 
 Input JSON:
 {cost_data}
 
 Output JSON:
 {
    "recommendations":  [
        {
           "title":  "...",
           "description":  "...",
           "estimated_savings_usd":  123.45,
           "priority":  "high|medium|low"
        }
    ]
 }
"""
 
 def  mock_cost_data():
       return  [
               {"service":  "Amazon EC2",  "cost":  120.5},
               {"service": "Amazon  RDS",  "cost":  80.2},
              {"service":  "Amazon  S3",  "cost": 45.7},
        ]
 
 def call_bedrock(cost_data):
        body  =  {
              "prompt":  PROMPT.format(cost_data=json.dumps(cost_data,  indent=2)),
               "max_tokens": 800,
        }
        response  = bedrock.invoke_model(
               modelId="anthropic.claude-3-sonnet-20240229-v1:0",
               body=json.dumps(body),
               contentType="application/json",
              accept="application/json",
        )
        payload  = json.loads(response["body"].read())
        text  =  payload.get("completion") or  payload.get("output_text")  or  ""
       return  text
 
 def parse_json_block(text:  str):
        try:
               start =  text.index("{")
               end  = text.rindex("}")  +  1
               return json.loads(text[start:end],  parse_float=Decimal)
        except  Exception:
              return  {"recommendations":  []}
 
def  store_recommendations(recs):
        now  = datetime.utcnow().isoformat()
        item  =  {
              "id":  now,
               "created_at":  now,
              "recommendations":  recs["recommendations"],
        }
        table.put_item(Item=item)
       return  item
 
 def lambda_handler(event,  context):
        cost_data  = mock_cost_data()
        raw  =  call_bedrock(cost_data)
       recs  =  parse_json_block(raw)
        stored =  store_recommendations(recs)
 
        return {
               "statusCode":  200,
               "body": json.dumps({"message":  "Recommendations  generated",  "item": stored},  default=str),
        }
