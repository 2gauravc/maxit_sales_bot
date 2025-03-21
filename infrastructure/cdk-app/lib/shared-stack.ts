import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';

export class SharedStack extends cdk.Stack {
    public readonly vpc: ec2.Vpc;
    public readonly ecsCluster: ecs.Cluster;

    constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // ✅ Create VPC
        this.vpc = new ec2.Vpc(this, 'OllamaVpc', {
            maxAzs: 2,
            subnetConfiguration: [{
                name: 'PublicSubnet',
                subnetType: ec2.SubnetType.PUBLIC,
            }],
            natGateways: 0
        });

        // ✅ Create ECS Cluster
        this.ecsCluster = new ecs.Cluster(this, 'OllamaCluster', { vpc: this.vpc });

        new cdk.CfnOutput(this, 'VpcId', { value: this.vpc.vpcId });
        new cdk.CfnOutput(this, 'EcsClusterName', { value: this.ecsCluster.clusterName });
    }
}
