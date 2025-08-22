import boto3
import time
import logging

# Constants / configuration
TABLE_NAME = "EmailCounters"
S3_BUCKET_URL = "https://is.api.varunjawarani.com"
TTL_DAYS = 90  # Expiration period in days
MAX_IMAGE = 50  # Maximum numbered image

# Initialize DynamoDB client
dynamodb = boto3.client("dynamodb")

def handler(event: dict, context) -> dict:
    try:
        logging.info(f"Event: {event}")
        logging.info(f"Request ID: {getattr(context, 'aws_request_id', 'unknown')}")

        # Extract query parameter
        params = event.get("queryStringParameters") or {}
        email_id = params.get("id")
        if not email_id:
            return {
                "statusCode": 400,
                "body": "Missing id parameter"
            }

        current_time = int(time.time())
        expires_at = current_time + TTL_DAYS * 24 * 3600

        # Increment per-email counter and set TTL if not exists
        response = dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={"pk": {"S": f"email#{email_id}"}},
            UpdateExpression="ADD #c :inc SET #ttl = if_not_exists(#ttl, :ttl)",
            ExpressionAttributeNames={
                "#c": "count",
                "#ttl": "expiresAt"
            },
            ExpressionAttributeValues={
                ":inc": {"N": "1"},
                ":ttl": {"N": str(expires_at)}
            },
            ReturnValues="UPDATED_NEW"
        )

        count = int(response["Attributes"]["count"]["N"])
        logging.info(f"Email {email_id} opened. Count: {count}")

        # Increment global counter
        dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={"pk": {"S": "global#total"}},
            UpdateExpression="ADD #c :inc",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":inc": {"N": "1"}}
        )

        # Determine which image to serve
        image_file = f"{count}.png" if count <= MAX_IMAGE else "50plus.png"
        redirect_url = f"{S3_BUCKET_URL}/{image_file}"

        return {
            "statusCode": 302,
            "headers": {
                "Location": redirect_url,
                "Cache-Control": "no-store"
            },
            "body": ""
        }

    except Exception as e:
        logging.error(f"Error in /open Lambda: {e}")
        return {
            "statusCode": 500,
            "body": "Internal server error"
        }
