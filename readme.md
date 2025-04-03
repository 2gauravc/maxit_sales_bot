# Maxit Bot

Maxit is a Corporate and Investment Banker's (CIB) assistant. To know more about the vision behind Maxit, visit the [Maxit Wiki](https://github.com/2gauravc/maxit_sales_bot/wiki)

This README will help you install 'your own' Maxit - yes your own CIB Sales Assistant.

## Install Maxit Infrastructure

Maxit uses AWS CDK and CloudFormation (IaC) templates for installation. You will need an AWS account to get started. 

**Step 1:** Identify your environment 

You can set this up on any environment - your own laptop / desktop or a Cloud IDE. 
I recommend setting this up on Github Codespaces. 

**Step 2:** Set-up your AWS credentials 

a) Check and Install the AWS CLI.   
Check if your environment already has the AWS CLI installed. 
```
aws --version
```

If you do not have the CLI installed, follow the steps here [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

b) Set up your AWS credentials     
Maxit will need permissions to create AWS resources on your behalf. Set up your AWS account credentials and the right region (where you intend to deploy the infra) using 

```
aws configure
```
Test the aws configuration 

```
aws sts get-caller-identity
```

**Step 3** Create a secret and store it in AWS Secrets Manager

This secret will be used by Bedrock Access Gateway to authenticate connections.  

a) Generate a secret using `openssl rand -hex 32

b) Store the secret in AWS Secrets Manager. 
- Open Secrets Manager using the AWS Management Console 
- Navigate to the right region - where you intend to deploy the infra 
- Save the secret 
- Note the Secret ARN


**Step 4** Clone the repo 

In a suitable directory clone the git repo (on Github codespaces this should be inside /workspaces/)
```
git clone https://github.com/2gauravc/maxit_sales_bot.git
```

**Step 5** Set up the AWS CDK 

Install the dependencies. 
```
cd maxit_sales_bot/infrastructure/cdk-app/
npm install 
```
Set-up the cdk. 

```
cdk bootstrap
cdk synth
```

**Step 6** Update the context variable  

Update the following context variables in the cdk.context.json file. 
- "s3BucketName": "XX", \\ This is the bucket to store the uploaded files 
  "s3BucketRegion": "us-east-1", \\ Region in which the bucket is created 
  "bedrockAccessGatewaysecretArn":"arn:aws:secretsmanager:<<region>>:<<account>>:secret:<<secret-name>>" \\ This is the arn of the secret (from Step 3)

**Step 7** Deploy the infrastructure 

```
cdk deploy
```

This will install 4 stacks and the following key end resources. 

| Stack | Key Output | How to use |
|----------|----------|----------|
| FrontEndStack   | OpenWebUI (on ECS Fargate)  | Launch ChatInterfaceURL |
| BackEndStack | Ollama Service (on ECS Fargate) | Use OllamaLoadBalancerURL to import models |
| SharedStack | VPC, Subnets, ECS Cluster  | NA  |
| BedrockStack | Bedrock Access Gateway  | Use APIBaseUrl to connect OpenWebUI to Bedrock Models  |

Notes: 
- The BackEndStack installs the Ollama service on CPU instances. For good performance with large models like Deepseek, switch to GPU on EC2 containers (Fargate does not support GPU)


## Configure the tools

1. Download a Model to OpenWebUI 

- Login to OpenWebUI by clicking on the 'ChatInterfaceURL' Output of the FrontEndStack 
- Download a model via ollama service endpoint. This model is hosted on ECS fargate containers. Since the model is locally hosted, it is best to go for a smaller model such as gemma:2b. Issue this command to download the model  

```
curl -X POST http://${ollamaService.loadBalancer.loadBalancerDnsName}/api/pull -d '{"name": "gemma:2b"}'
```

2) Add Bedrock Access Gateway connection 
- On the admin panel,open 'Connections'
- Add a new OpenAI connection 
- Enter the APIBaseURL (output of the Bedrock Stack) and the secret key you generated in Step 3. 

3) Enable Web search on OpenWebUI 

- On OpenWebUI front end go to 'Admin Panel'-> 'Settings' -> 'Web Search'. Provide the [Tavily](https://tavily.com/) API key and toggle on 'Web Search'

