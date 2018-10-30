import boto3

# Create an SNS client
sns = boto3.client(
	'sns',
	aws_access_key_id='AKIAIL7SBOJ2DA3ONVKQ',
    aws_secret_access_key='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',
    region_name='us-east-1'
    )

# Send a SMS message to the specified phone number
response = sns.publish(
    PhoneNumber='1-678-524-6213',
    Message='Sanus Solutions Alert: Luka, you need to focus now.',
)

# Print out the response
print(response)