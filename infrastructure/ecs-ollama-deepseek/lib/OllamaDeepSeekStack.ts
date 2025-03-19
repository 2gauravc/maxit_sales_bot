import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

export class OllamaDeepSeekStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create VPC with only public subnets
    const vpc = new ec2.Vpc(this, 'OllamaVpc', {
      maxAzs: 2,
      subnetConfiguration: [{
        name: 'PublicSubnet',
        subnetType: ec2.SubnetType.PUBLIC,
      }],
      natGateways: 0
    });

    // Create ECS Cluster
    const cluster = new ecs.Cluster(this, 'OllamaCluster', { vpc });

    // Ollama Service
    const ollamaService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'OllamaService', {
      cluster,
      cpu: 4096,
      memoryLimitMiB: 16384,
      desiredCount: 1,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry('ollama/ollama:latest'),
        containerPort: 11434,
        environment: { 'OLLAMA_HOST': '0.0.0.0' },
        enableLogging: true,
      },
     
      publicLoadBalancer: true,
      assignPublicIp: true
    });

  

    // WebUI Service
    const webuiService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'WebUI', {
      cluster,
      cpu: 4096,
      memoryLimitMiB: 16384,
      desiredCount: 1,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry('ghcr.io/open-webui/open-webui:main'),
        containerPort: 8080,
        environment: {
          'OLLAMA_BASE_URL': `http://${ollamaService.loadBalancer.loadBalancerDnsName}`,
          'WEBUI_SECRET_KEY': '116c18c173abec27b25973f2d1fbff14ca6329f22b3d4faaae6ea7fc8697d928',
          'MODEL_FILTER_ENABLED': 'false', // Show all models
          'WEBUI_DEBUG_MODE': 'true', // Debugging
          'OLLAMA_API_OVERRIDE_BASE_URL': `http://${ollamaService.loadBalancer.loadBalancerDnsName}`,
          'ENABLE_OLLAMA_MANAGEMENT': 'true'
        },
      
        enableLogging: true
      },
      publicLoadBalancer: true,
      assignPublicIp: true
    });

    
    // Security Configuration
    ollamaService.service.connections.allowFrom(
      webuiService.service,
      ec2.Port.tcp(11434)
    );

    // Health Checks
    ollamaService.targetGroup.configureHealthCheck({
      path: '/',
      port: '11434',
      timeout: cdk.Duration.minutes(2),
      interval: cdk.Duration.minutes(4),
      healthyThresholdCount: 2,
      unhealthyThresholdCount: 3
    });

    webuiService.targetGroup.configureHealthCheck({
      path: '/',
      healthyHttpCodes: '200-399',
    });

    // HTTPS Configuration (Uncomment with valid ACM cert ARN)
    // webuiService.loadBalancer.addListener('HTTPS', {
    //   port: 443,
    //   certificates: [/* Your ACM cert ARN */],
    //   defaultAction: elbv2.ListenerAction.forward([webuiService.targetGroup])
    // });

    // Outputs
    new cdk.CfnOutput(this, 'ChatInterfaceURL', {
      value: webuiService.loadBalancer.loadBalancerDnsName
    });

    new cdk.CfnOutput(this, 'ModelPullCommand', {
      value: `curl -X POST http://${ollamaService.loadBalancer.loadBalancerDnsName}/api/pull -d '{"name": "deepseek-r1:7b"}'`
    });
  }
}
