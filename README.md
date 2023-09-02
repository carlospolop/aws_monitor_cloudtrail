# AWS Monitor CloudTrail

Very basic CloudTrail logs monitor via CLI.

This script will basically **recheck the CloudTrail logs every 20s and print information only about the new events**.

## Quick Start

```bash
# Get help
python3 aws_monitor_cloudtrail.py  -h
usage: aws_monitor_cloudtrail.py [-h] profile bucket

Monitor CloudTrail logs in an S3 bucket.

positional arguments:
  profile     AWS CLI profile to use.
  bucket      Name of the S3 bucket where CloudTrail logs are stored.

options:
  -h, --help  show this help message and exit

# Run monitoring
python3 aws_monitor_cloudtrail.py "profile" "aws-cloudtrail-logs-<rest-cloudtrail-bucket-name>"

# Focus on a user or role
python3 aws_monitor_cloudtrail.py "profile" "aws-cloudtrail-logs-<rest-cloudtrail-bucket-name>" | grep -i "user/role-name"
```