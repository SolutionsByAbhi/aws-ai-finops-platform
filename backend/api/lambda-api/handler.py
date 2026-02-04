 import  json
 from routers.cost  import  get_costs
 from routers.recommendations  import  get_recommendations
 
def  lambda_handler(event,  context):
        route =  event.get("rawPath")  or  event.get("path", "/")
        method  =  event.get("requestContext", {}).get("http",  {}).get("method")  or  event.get("httpMethod", "GET")
 
        if  route.endswith("/costs") and  method  ==  "GET":
              body,  status  =  get_costs()
       elif  route.endswith("/recommendations")  and  method ==  "GET":
               body,  status =  get_recommendations()
        else:
               body, status  =  {"message":  "Not found"},  404
 
        return {
               "statusCode":  status,
               "headers": {"Content-Type":  "application/json"},
               "body":  json.dumps(body, default=str),
        }
