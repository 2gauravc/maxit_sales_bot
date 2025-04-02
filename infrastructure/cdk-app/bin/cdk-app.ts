#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { SharedStack } from '../lib/shared-stack';
import { BackendStack } from '../lib/backend-stack';
import { FrontendStack } from '../lib/frontend-stack';
import { BedrockStack } from '../lib/bedrock-stack';
const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION
};

const app = new cdk.App();
cdk.Tags.of(app).add('Project', 'Maxit');

// ✅ Deploy Shared Infrastructure First
const sharedStack = new SharedStack(app, 'SharedStack', { env });

//Deploy the Bedrock Access Gateway 
const bedrockStack = new BedrockStack(app, 'BedrockStack', {
    vpc: sharedStack.vpc, // 👈 reuse existing VPC
    env 
  });
bedrockStack.addDependency(sharedStack);

// ✅ Deploy Backend (Ollama Service)
const backendStack = new BackendStack(app, 'BackendStack', {
    vpc: sharedStack.vpc,
    ecsCluster: sharedStack.ecsCluster, 
    env
});
backendStack.addDependency(sharedStack);

// ✅ Deploy Frontend (WebUI)
const frontendStack = new FrontendStack(app, 'FrontendStack', {
    vpc: sharedStack.vpc,
    ecsCluster: sharedStack.ecsCluster,
    ollamaLoadBalancerDnsName: backendStack.ollamaLoadBalancerDnsName,  // ✅ Passing String, Not Full Object
    s3BucketName: 'ppt-bkt',
    env
});
frontendStack.addDependency(backendStack);
frontendStack.addDependency(sharedStack);
