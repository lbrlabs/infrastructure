import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as github from "@pulumi/github";


// create an oidc provider that allows access from this repo
const oidcProvider = new aws.iam.OpenIdConnectProvider("infrastructureAdmin", {
  thumbprintLists: ["6938fd4d98bab03faadb97b34396831e3780aea1"],
  clientIdLists: ["https://github.com/jaxxstorm", "sts.amazonaws.com"],
  url: "https://token.actions.githubusercontent.com",
});

// create an IAM role that is associated with this repo
// allows the OIDC provider to use it
const role = new aws.iam.Role("infrastructureAdmin", {
  description: "Access to AWS for github.com/jaxxstorm/lbrlabs",
  assumeRolePolicy: {
    Version: "2012-10-17",
    Statement: [
      {
        Action: ["sts:AssumeRoleWithWebIdentity"],
        Effect: "Allow",
        Condition: {
          StringLike: {
            "token.actions.githubusercontent.com:sub":
              "repo:jaxxstorm/lbrlabs:*", // replace with your repo
          },
        },
        Principal: {
          Federated: [oidcProvider.arn],
        },
      },
    ],
  } as aws.iam.PolicyDocument,
});

// create a policy that allows us to assumeRole to any other role
const policy = new aws.iam.Policy("infrastructureAdmin", {
  policy: {
    Version: "2012-10-17",
    Statement: [
      {
        Action: ["sts:*"], // FIXME: can we limit this to an org maybe?
        Effect: "Allow",
        Resource: "*",
      },
    ],
  } as aws.iam.PolicyDocument,
}, { parent: role });

// attach the policy
new aws.iam.PolicyAttachment("infrastructureAdmin", {
    policyArn: policy.arn,
    roles: [ role.id ]
}, { parent: policy })

// set the role arn in GitHub secrets
new github.ActionsSecret("aws", {
    repository: "lbrlabs",
    secretName: "ROLE_ARN",
    plaintextValue: role.arn,
  });


