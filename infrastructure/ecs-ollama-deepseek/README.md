# Deploying DeepSeek R1 on ECS Fargate with Open WebUI: A Scalable Ollama based AI ChatBot

A complete CDK Automation with DeepSeek R1 Chatbot confined locally inside AWS ECS Fargate container running Ollama that doesn't transmit your data to China!

# Architecture Diagram
![Alt text](./ollama-deepseek-architecture.png?raw=true "Ollama with DeepSeek on AWS Fargate")

For more details on how to deploy the infrastructure and solution details, please refer to the Blog Post:

* [Deploying DeepSeek R1 on ECS Fargate with Open WebUI: A Scalable Ollama based AI ChatBot](https://vivek-aws.medium.com/deploying-deepseek-r1-on-ecs-fargate-with-open-webui-a-scalable-ollama-ai-solution-0008049a73a9).

## Pro Tip 💡
Add a new LLM to your Ollama container by simply running the following curl command:
```sh
curl -X POST http://<OLLAMA_LB_DNS>/api/pull -d '{"name": "your-model-name"}'

Replace "your-model-name-here" with any supported LLM (e.g., deepseek-r1:1.5b, mistral:7b)
```


## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
