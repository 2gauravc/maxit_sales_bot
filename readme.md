# Maxit Bot

This is the repo for Maxit Sales bot. 

Stack 1: 

<img src="architecture/maxit.drawio.png" alt="Alt Text" style="max-width: 20%; max-height: 20%; cursor: zoom-in;">

Order of build: 

1. S3 bucket set-up (tag: maxit)
``` 
aws s3api create-bucket --bucket maxit-bot-annualreports --region us-east-2 
aws s3api put-bucket-tagging --bucket maxit-bot-annualreports --tagging 'TagSet=[{Key=project,Value=maxit}]'
```

2. DynamoDB set-up - Metadata DB (tag: maxit)
3. Lambda - Extract Metadata (tag: maxit)
4. Document DB - Client Insights DB (tag: maxit)
5. Lambda - Extract client insights (tag: maxit)
6. Lambda - Poll Edgar (tag: maxit)
7. Event bridge set-up to trigger "Lambda - Poll Edgar" daily 



