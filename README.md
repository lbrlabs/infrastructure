# lbrlabs

This repo is designed to serve two purposes:
  - Serve as a reference example for how to run complex, "production grade" infrastructure with Pulumi
  - Manage my personal infrastructure via [Pulumi](https://pulumi.com)

While I've endeavored to keep this "production grade" where I can, I also don't want to spend a fortune. Cost takes precedent over production ready where the trade-off is required.

## Notable Features

This repository contains a lot of things that I think would be a good reference for any AWS-based infrastructure:

As of writing, you can find the following:

- Configured to use continuous delivery via [GitHub Actions](https://github.com/features/actions)
    - Uses the [Pulumi GitHub Action](https://www.pulumi.com/docs/guides/continuous-delivery/github-actions/)
- Credentials access to cloud providers is as secure as I think I can make it (suggestions welcome via issues)
    - AWS Access is managed via [OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) - more information on configuring this can be found [here](https://leebriggs.co.uk/blog/2022/01/23/gha-cloud-credentials)
        - Access to all accounts is done via [Assume Role](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
    - Other cloud provider credentials are configured via [Pulumi secret encryption](https://www.pulumi.com/docs/intro/concepts/secrets/)
- Multiple cloud providers are managed
    - My domains are hosted by [Cloudflare](https://cloudflare.com)
        - I designate subdomains for cloud providers, all done via a single Pulumi program
- A best practice multi-account AWS network is configured
    - A transit gateway is deployed to a dedicated "shared services" account

## Not Included Here

Some parts of my infrastructure were not configured here or via Pulumi:

### AWS SSO

[AWS SSO](https://aws.amazon.com/single-sign-on/) is configured, with [auth0](https://auth0.com) as the backing IdP. This was not configured via Pulumi because AWS SSO doesn't have APIs to perform the operations, and is not in any Pulumi provider

### AWS Control Tower

An [AWS Organization](https://aws.amazon.com/organizations/) is configured using [AWS Control Tower](https://aws.amazon.com/controltower/). I briefly considered configuring this with Pulumi using a third-party provider but decided to keep with Control Tower for now. This may change in the future.

## Projects

All projects are in subdirectories and have specific purposes. I've followed a [monorepo pattern](https://www.pulumi.com/docs/guides/organizing-projects-stacks/#monolithic) for configuring my Pulumi programs.

Each project has a detailed `README`. You can find a summary of their purpose below.

### Delivery

The delivery Pulumi project is a project which bootstraps IAM permissions for GitHub Actions to run Pulumi programs across all accounts in the AWS Organization.

You can read more about this program [here](delivery/README.md)

### Domains

The domains Pulumi project is a project which manages all of the domain names which I own. These domains are currently in Cloudflare, and I've designated subdomains for some purposes in some cloud provider DNS providers

You can read more about this program [here](domains/README.md)

### Network

The network Pulumi project is a project which creates an [AWS Transit Gateway](https://aws.amazon.com/transit-gateway/) and VPCs in all AWS accounts in the organization which will run workloads.

You can read more about this program [here](network/README.md)

### Wildcard Certificate

The wildcard certificate Pulumi project is a project which creates a wildcard certificate via [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/).

You can read more about this program [here](certificate_manager/README.md)




