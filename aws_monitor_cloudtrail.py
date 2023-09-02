import boto3
import time
import gzip
from io import BytesIO

def get_initial_logs(profile, bucket_name, prefix='AWSLogs/'):
    """Get all initial logs in the bucket."""
    session = boto3.Session(profile_name=profile)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    return {obj.key for obj in bucket.objects.filter(Prefix=prefix) if not (obj.key.startswith("CloudTrail-Digest/") or obj.key.startswith("CloudTrail-Insight/"))}

def process_log_content(content):
    # Decompress the gzipped log content
    with gzip.GzipFile(fileobj=BytesIO(content)) as gzipfile:
        log_data = gzipfile.read().decode('utf-8')

    # Parse the JSON content
    log_json = json.loads(log_data)

    # Extract and print the desired details for each event
    for record in log_json['Records']:
        arn = record.get('userIdentity', {}).get('arn', 'N/A')
        event_source = record.get('eventSource', 'N/A')
        event_name = record.get('eventName', 'N/A')
        print(f"ARN: {arn}, Event Source: {event_source}, Event Name: {event_name}")

def monitor_cloudtrail_logs(profile, bucket_name, prefix='AWSLogs/'):
    """Monitor CloudTrail logs in the provided S3 bucket."""

    print(f"Monitoring CloudTrail logs...")
    # Establish a boto3 session with the provided profile
    session = boto3.Session(profile_name=profile)

    # Connect to the S3 resource using the session
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # Get all existing logs before starting to monitor
    processed_logs = get_initial_logs(profile, bucket_name, prefix)
    print(f"Found {len(processed_logs)} existing logs.")

    while True:
        for obj in bucket.objects.filter(Prefix=prefix):
            # Avoid processing objects in "CloudTrail-Digest/" and "CloudTrail-Insight/" folders
            if "CloudTrail-Digest/" in obj.key or "CloudTrail-Insight/" in obj.key:
                continue

            # Check if we haven't processed this log before
            if obj.key not in processed_logs:
                content = obj.get().get('Body').read()
                process_log_content(content)
                # Add the log key to our set of processed logs
                processed_logs.add(obj.key)

        # Sleep for 5 seconds before checking for new logs
        time.sleep(20)

if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Monitor CloudTrail logs in an S3 bucket.")
    parser.add_argument('profile', help='AWS CLI profile to use.')
    parser.add_argument('bucket', help='Name of the S3 bucket where CloudTrail logs are stored.')
    args = parser.parse_args()

    monitor_cloudtrail_logs(args.profile, args.bucket)
