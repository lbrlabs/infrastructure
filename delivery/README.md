# Delivery

This contains a Pulumi program that bootstraps the permissions for the organization so we can deploy Pulumi programs via continuous delivery.

This Pulumi program does not run via the GitHub actions continuous delivery, as it requires elevated permissions which are not designated to the GitHub Action. It is designed to be run by an administrator.

It creates multiple resources, these have been documented in the comments. An overhead of each can be found below.

## OIDC Provider

The OIDC provider allows GitHub to access AWS and grab temporary credentials.

## Infrastructure Admin IAM Role

This role is associated with the OIDC provider. It allows access by our specific GitHub repo and is used when GitHub Actions grabs credentials.

There is a policy attached to the role which _only_ allows the role to assume roles to other roles. The role itself cannot perform any other action except assume role to other roles in the AWS Organization

We store the role ARN that's created into a GitHub Action secret, so the GitHub Action workflow can easily retrieve it.

## Infrastructure Role

The infrastructure role exists in all AWS accounts, and the Infrastructure Admin role assumes role into that role.

In order to ease the rollout of this role, it is defined via a [CloudFormation [StackSet](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html) which ensures that any new account that is added to the AWS Organization will have an infrastructure role that exists in it when it's created.

This allows easy management of resources in any AWS account in the organization

## Enhancement Opportunities

Currently, the CloudFormation StackSet has an account ID and role name hardcoded into it. We should populate that automatically.
