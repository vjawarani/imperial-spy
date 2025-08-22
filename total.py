import boto3
import json
import logging

# Constants / configuration
TABLE_NAME = "EmailCounters"
COUNTER_KEY = "global#total"
WEBFLOW_DOMAIN = "https://www.varunjawarani.com"

# Initialize DynamoDB client
dynamodb = boto3.client("dynamodb")

# Standard headers for CORS
HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": WEBFLOW_DOMAIN
}

def handler(event: dict, context) -> dict:
    try:
        logging.info(f"Event: {event}")
        logging.info(f"Request ID: {getattr(context, 'aws_request_id', 'unknown')}")

        response = dynamodb.get_item(
            TableName=TABLE_NAME,
            Key={"pk": {"S": COUNTER_KEY}}
        )

        item = response.get("Item")
        total = int(item.get("count", {"N": "0"})["N"]) if item else 0

        logging.info(f"Total count retrieved: {total}")

        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"total": total})
        }

    except Exception as e:
        logging.error(f"Error retrieving total count: {e}")
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": "Internal server error"})
        }
