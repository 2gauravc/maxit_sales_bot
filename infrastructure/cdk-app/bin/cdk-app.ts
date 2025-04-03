#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { SharedStack } from '../lib/shared-stack';
import { BackendStack } from '../lib/backend-stack';
import { FrontendStack } from '../lib/frontend-stack';
import { BedrockStack } from '../lib/bedrock-stack';

const app = new cdk.App();

// ✅ Reusable context getter
function requireContext(app: cdk.App, key: string): string {
  const value = app.node.tryGetContext(key);
  if (!value) {
    throw new Error(`Missing context: ${key}. Please add it to cdk.context.json or pass with --context`);
  }
  return value;
}

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION
};

cdk.Tags.of(app).add('Project', 'Maxit');

const s3BucketName = requireContext(app, 's3BucketName');
const s3BucketRegion = requireContext(app, 's3BucketRegion');
const secretArn = requireContext(app, 'bedrockAccessGatewaysecretArn');


// ✅ Deploy Shared Infrastructure First
const sharedStack = new SharedStack(app, 'SharedStack', { env });

//Deploy the Bedrock Access Gateway 
const bedrockStack = new BedrockStack(app, 'BedrockStack', {
    vpc: sharedStack.vpc, // 👈 reuse existing VPC
    secretArn,
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
    s3BucketName,
    s3BucketRegion,
    env
});

frontendStack.addDependency(backendStack);
frontendStack.addDependency(sharedStack);
