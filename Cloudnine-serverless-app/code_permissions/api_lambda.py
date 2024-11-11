import json
import boto3
from decimal import Decimal

# Initialize clients
stepfunctions = boto3.client('stepfunctions')

# Replace with your Step Function ARN
STEP_FUNCTION_ARN = "YOUR_STEP_FUNCTION_ARN"

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        flightNumber = body.get('flightNumber')
        email = body.get('email')
        waitSeconds = body.get('waitSeconds')

        # Validate required fields
        if not flightNumber or not email or waitSeconds is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Flight number, email, and waitSeconds are required')
            }

        # Schedule a reminder using Step Functions with wait time
        response = stepfunctions.start_execution(
            stateMachineArn=STEP_FUNCTION_ARN,
            input=json.dumps({
                "waitSeconds": waitSeconds,
                "message": f"Flight {flightNumber} status update for {email}",
                "email": email
            }, cls=DecimalEncoder)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Reminder scheduled successfully!',
                'executionArn': response['executionArn']
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
