import urllib3
import json

def handler(event, context):
    print("Received event:", json.dumps(event))
    try:
        lb_url = event['ResourceProperties']['Url']
        model_name = event['ResourceProperties']['Model']

        http = urllib3.PoolManager()
        res = http.request(
            "POST",
            f"http://{lb_url}/api/pull",
            body=json.dumps({"name": model_name}),
            headers={'Content-Type': 'application/json'}
        )

        print(f"Response status: {res.status}")
        print(f"Response data: {res.data}")

        if res.status == 200:
            return {
                'Status': 'SUCCESS',
                'StatusCode': res.status
            }
        else:
            raise Exception(f"Failed to pull model: {res.status} {res.data}")
    
    except Exception as e:
        print(f"Error: {e}")
        raise e

if __name__ == "__main__":
    print("Running local test...")

    test_event = {
        "RequestType": "Create",
        "ResponseURL": "http://pre-signed-S3-url-for-response",  # won't be used here
        "StackId": "dummy-stack-id",
        "RequestId": "dummy-request-id",
        "ResourceType": "Custom::ModelPuller",
        "LogicalResourceId": "ModelPuller",
        "ResourceProperties": {
            "Url": "backen-ollam-nvzzjhyuiul5-1731158572.us-east-2.elb.amazonaws.com",
            "Model": "orca-mini:3b"
        }
    }

    response = handler(test_event, None)
    print("Lambda response:", response)

