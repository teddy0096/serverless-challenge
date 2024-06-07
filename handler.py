import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
dbtable = dynamodb.Table('TodoListTable')

def Hello(event, context):
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def Test(event, context):
    body = {
        "message": "Hello, world! This is a test method asdasdas."
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def CreateTodo(event, context):
    try:
        # Access the JSON payload directly from the event dictionary
        parsed_body = json.loads(event['body'])
        
        # Print the parsed body for debugging purposes
        print('Parsed Body:', parsed_body)
        
        # Process the parsed body as needed

        entry = {
            'todoID': parsed_body['todoID'],
            'userId': parsed_body['userId'],
            'TaskName': parsed_body['TaskName'],
            'Description': parsed_body['Description'],
            'TimeLeft': parsed_body['TimeLeft'],
            'completed': parsed_body['completed'],
            'StartDate': parsed_body['StartDate'],
            'EndDate': parsed_body['EndDate'],
            'CreatedAt': parsed_body['CreatedAt']
        }

        dbtable.put_item(Item=entry)
        
        # Return a response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Todo item created successfully'})
        }
    except KeyError:
        # Handle the case when 'body' key is not found in the event dictionary
        print('Error: Missing body key in the event dictionary')
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing body key in the event dictionary'})
        }
    except json.JSONDecodeError:
        # Handle the case when the JSON payload cannot be decoded
        print('Error: Unable to parse JSON payload')
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unable to parse JSON payload'})
        }
    
def GetTodoList(event, context):
    try:
        # Perform a scan operation to retrieve all items from the table
        response = dbtable.scan()
        print('scanned response', response)

        # Extract the items from response
        items = response['Items']
        print('extracted item', items)

        # Convert the Decimal value to float
        items = [{k: convert_decimal_to_float(v) if isinstance(v, Decimal) else v for k, v in item.items()} for item in items]

        # Return the items
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items})
        }

    except Exception as e:
        # handle any exception
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# def GetTodoListById(event, context):
#     try:
#         key_condition_expression = Key('partition_key_name').eq()
#     except Exception as e:
#         print('Error:', e)
   
def convert_decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError