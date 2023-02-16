import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const stack = pulumi.getStack();
const config = new pulumi.Config();
const cidrBlock = config.require("cidrBlock");
const enableNatGateways = config.requireBoolean("enableNatGateways");
const numberOfAvailabilityZones = config.requireNumber(
  "numberOfAvailabilityZones"
);

let natGatewayStrategy: awsx.ec2.NatGatewayStrategy;

if (enableNatGateways) {
  natGatewayStrategy = awsx.ec2.NatGatewayStrategy.Single;
} else {
  natGatewayStrategy = awsx.ec2.NatGatewayStrategy.None;
}

const vpc = new awsx.ec2.Vpc(`${stack}-vpc`, {
  cidrBlock: cidrBlock,
  subnetSpecs: [
    {
      type: "Public",
    },
    {
      type: "Private",
    },
  ],
  numberOfAvailabilityZones: numberOfAvailabilityZones,
  natGateways: {
    strategy: natGatewayStrategy,
  },
  tags: {
    Stack: stack,
    Github: "jaxxstorm/lbrlabs",
  },
});

export const vpcId = vpc.vpcId;
export const publicSubnetIds = vpc.publicSubnetIds;
export const privateSubnetIds = vpc.privateSubnetIds;
