import os
import  boto3
from boto3.dynamodb.conditions  import  Key

TABLE_NAME  =  os.environ["RECOMMENDATION_TABLE"]
dynamodb =  boto3.resource("dynamodb")
table  = dynamodb.Table(TABLE_NAME)

def  get_recommendations():
      resp  =  table.scan(Limit=10)
       items =  sorted(resp.get("Items",  []),  key=lambda x:  x["created_at"],  reverse=True)
       return {"items":  items},  200
