import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as tgw from "./sharedTransitGateway";
import * as vpc from "./transitGatewayAttachedVpc";

const devProvider = new aws.Provider("dev", {
  assumeRole: {
    duration: "1h",
    roleArn: "arn:aws:iam::565485516070:role/infrastructure",
    sessionName: "lbrlabs",
  },
});
const transitProvider = new aws.Provider("shared_services", {
  assumeRole: {
    duration: "1h",
    roleArn: "arn:aws:iam::587571862190:role/infrastructure",
    sessionName: "lbrlabs",
  },
});

const prodProvider = new aws.Provider("prod", {
  assumeRole: {
    duration: "1h",
    roleArn: "arn:aws:iam::780219548054:role/infrastructure",
    sessionName: "lbrlabs",
  },
});

const transitGw = new tgw.SharedTransitGateway(
  "tgw",
  {
    sharePrincipal:
      "arn:aws:organizations::609316800003:organization/o-fjlzoklj5f",
  },
  { provider: transitProvider, parent: transitProvider }
);

const transitVpc = new vpc.TransitGatewayAttachedVpc(
  "transit",
  {
    cidrBlock: "172.20.0.0/22",
    transitGatewayId: transitGw.transitGateway.id,
  },
  { provider: transitProvider, parent: transitProvider, dependsOn: transitGw }
);

const devVpc = new vpc.TransitGatewayAttachedVpc(
  "dev",
  {
    cidrBlock: "172.19.0.0/22",
    transitGatewayId: transitGw.transitGateway.id,
  },
  { provider: devProvider, parent: devProvider, dependsOn: transitGw }
);

const prodVpc = new vpc.TransitGatewayAttachedVpc(
  "prod",
  {
    cidrBlock: "172.18.0.0/22",
    transitGatewayId: transitGw.transitGateway.id,
  },
  { provider: prodProvider, parent: prodProvider, dependsOn: transitGw }
);
