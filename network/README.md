# Network

This Pulumi project creates an [AWS Transit Gateway, VPCs, and attachments for the transit gateway into those VPCs. It is designed to allow traffic to flow through an AWS Organization between VPCs.

It leverages multiple Pulumi features to make this easier

- It uses a [Component Resource](https://www.pulumi.com/docs/intro/concepts/resources/components/) to create abstractions for the transit gateway
- It leverages multiple [resource providers](https://www.pulumi.com/docs/intro/concepts/resources/providers/#explicit-provider-configuration) to deploy all of the components needed in one Pulumi program

