import boto3
import os

# Get environment variables
bucket_name = os.environ['S3_BUCKET_NAME']
region = os.environ['AWS_REGION']

# Optional: You can set this dynamically if needed
output_filename = os.environ.get('OUTPUT_FILENAME', 'output.mp3')
s3_key = f"polly-audio/{output_filename}"

# Read text to synthesize
with open('speech.txt', 'r') as file:
    text = file.read()

# Initialize Polly and S3 clients
polly = boto3.client('polly', region_name=region)
s3 = boto3.client('s3', region_name=region)

# Synthesize speech using Amazon Polly
response = polly.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna'  # You can change voice here
)

# Save mp3 temporarily
with open('/tmp/' + output_filename, 'wb') as file:
    file.write(response['AudioStream'].read())

# Upload to S3
s3.upload_file(
    Filename='/tmp/' + output_filename,
    Bucket=bucket_name,
    Key=s3_key
)

print(f"Uploaded {output_filename} to s3://{bucket_name}/{s3_key}")