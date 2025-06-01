import boto3

def synthesize_speech(input_file, output_file, voice_id="Joanna"):
    # Read the text from the input file
    with open(input_file, "r") as f:
        text = f.read()

    # Create a Polly client
    polly = boto3.client("polly")

    # Request speech synthesis
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id
    )

    # Save the audio stream to a file
    with open(output_file, "wb") as f:
        f.write(response["AudioStream"].read())

    print(f"✅ Audio saved to {output_file}")

def upload_to_s3(file_name, bucket_name, object_name):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"✅ Uploaded {file_name} to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")

if __name__ == "__main__":
    bucket = "polly-learning-co"  # Replace with your S3 bucket name
    local_file = "speech.mp3"
    s3_object = "polly-audio/speech.mp3"  # The prefix + file name on S3

    synthesize_speech("speech.txt", local_file)
    upload_to_s3(local_file, bucket, s3_object)