#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { SharedStack } from '../lib/shared-stack';
import { BackendStack } from '../lib/backend-stack';
import { FrontendStack } from '../lib/frontend-stack';

const app = new cdk.App();

// ✅ Deploy Shared Infrastructure First
const sharedStack = new SharedStack(app, 'SharedStack');

// ✅ Deploy Backend (Ollama Service)
const backendStack = new BackendStack(app, 'BackendStack', {
    vpc: sharedStack.vpc,
    ecsCluster: sharedStack.ecsCluster
});
backendStack.addDependency(sharedStack);

// ✅ Deploy Frontend (WebUI)
const frontendStack = new FrontendStack(app, 'FrontendStack', {
    vpc: sharedStack.vpc,
    ecsCluster: sharedStack.ecsCluster,
    ollamaLoadBalancerDnsName: backendStack.ollamaLoadBalancerDnsName  // ✅ Passing String, Not Full Object
});
frontendStack.addDependency(backendStack);
frontendStack.addDependency(sharedStack);
