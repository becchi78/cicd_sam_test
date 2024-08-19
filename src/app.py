import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    # Get the bucket name and key (file name) from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    logger.info(
        f"Processing file {key} from bucket {bucket}"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(
            f"File {key} processed successfully from bucket {bucket}"
        )
    }
