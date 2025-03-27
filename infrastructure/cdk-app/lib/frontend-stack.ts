import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';

interface FrontendStackProps extends cdk.StackProps {
    vpc: ec2.Vpc;
    ecsCluster: ecs.Cluster;
    ollamaLoadBalancerDnsName: string;  // ✅ Receiving Only ALB DNS Name (String)
}

export class FrontendStack extends cdk.Stack {
    constructor(scope: cdk.App, id: string, props: FrontendStackProps) {
        super(scope, id, props);

        // ✅ WebUI Service (ECS Fargate)
        const webuiService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'WebUIService', {
            cluster: props.ecsCluster,
            cpu: 4096,
            memoryLimitMiB: 16384,
            desiredCount: 1,
            taskImageOptions: {
                image: ecs.ContainerImage.fromRegistry('ghcr.io/open-webui/open-webui:main'),
                containerPort: 8080,
                environment: {
                    'OLLAMA_BASE_URL': `http://${props.ollamaLoadBalancerDnsName}`,
                    'WEBUI_SECRET_KEY': '116c18c173abec27b25973f2d1fbff14ca6329f22b3d4faaae6ea7fc8697d928',
                    'MODEL_FILTER_ENABLED': 'false',
                    'WEBUI_DEBUG_MODE': 'true',
                    'OLLAMA_API_OVERRIDE_BASE_URL': `http://${props.ollamaLoadBalancerDnsName}`,
                    'ENABLE_OLLAMA_MANAGEMENT': 'true',
                    'STORAGE_PROVIDER':'s3', 
                    'S3_ENDPOINT_URL': 'https://s3.us-east-1.amazonaws.com',
                    'S3_REGION_NAME': 'us-east-1',
                    'S3_BUCKET_NAME':'ppt-bkt'
                },
                enableLogging: true
            },
            publicLoadBalancer: true,
            assignPublicIp: true
        });
        webuiService.loadBalancer.setAttribute('idle_timeout.timeout_seconds', '300');
        new cdk.CfnOutput(this, 'ChatInterfaceURL', {
            value: webuiService.loadBalancer.loadBalancerDnsName
        });
    }
}
