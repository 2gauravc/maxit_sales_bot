import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';

interface BackendStackProps extends cdk.StackProps {
    vpc: ec2.Vpc;
    ecsCluster: ecs.Cluster;
}

export class BackendStack extends cdk.Stack {
    public readonly ollamaLoadBalancerDnsName: string;

    constructor(scope: cdk.App, id: string, props: BackendStackProps) {
        super(scope, id, props);

        // ✅ Ollama Service (ECS Fargate)
        const ollamaService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'OllamaService', {
            cluster: props.ecsCluster,
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

        // ✅ Store Load Balancer DNS Name (String Only!)
        this.ollamaLoadBalancerDnsName = ollamaService.loadBalancer.loadBalancerDnsName;

        new cdk.CfnOutput(this, 'OllamaLoadBalancerURL', {
            value: this.ollamaLoadBalancerDnsName
        });
    }
}
