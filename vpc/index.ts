import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const vpc = new awsx.ec2.Vpc("briggs", {
  cidrBlock: "172.16.0.0/16",
  subnetSpecs: [
    {
      type: "Public",
    },
    {
      type: "Private",
    },
  ],
  numberOfAvailabilityZones: 3,
  natGateways: {
    strategy: awsx.ec2.NatGatewayStrategy.Single,
  },
  tags: {
    Name: "brig.gs",
    Project: "kutt",
  }
});

export const vpcId = vpc.vpcId;
export const publicSubnetIds = vpc.publicSubnetIds;
export const privateSubnetIds = vpc.privateSubnetIds;

