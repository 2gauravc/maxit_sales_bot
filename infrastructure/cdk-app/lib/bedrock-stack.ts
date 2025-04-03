import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as cfn_inc from 'aws-cdk-lib/cloudformation-include';
import * as path from 'path';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

interface BedrockStackProps extends cdk.StackProps {
  vpc: ec2.Vpc;
  secretArn: string;
}

export class BedrockStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: BedrockStackProps) {
    super(scope, id, props);
    const vpc = props.vpc;
    new cfn_inc.CfnInclude(this, 'BedrockAccessGatewayTemplate', {
      templateFile: path.join(__dirname, '../assets/bedrock-access-gateway.yaml'),
      parameters: {
        ApiKeySecretArn: props.secretArn,
        DefaultModelId: 'us.amazon.nova-pro-v1:0',
        VpcId: props.vpc.vpcId,
        PublicSubnet1: props.vpc.publicSubnets[0].subnetId,
        PublicSubnet2: props.vpc.publicSubnets[1].subnetId
      }
    });
  }
}