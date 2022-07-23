import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as tgw from "./sharedTransitGateway";
import * as vpc from "./transitGatewayAttachedVpc";

const devProvider = new aws.Provider("dev", {
  profile: "personal-development",
});
const transitProvider = new aws.Provider("shared_services", {
  profile: "personal-shared_services",
});

const prodProvider = new aws.Provider("prod", {
  profile: "personal-production",
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

