# Certificate Manager

This is a fairly simple Pulumi program that creates a wildcard certificate for the `*.aws.lbrlabs.com` domain.

## Enhancement Opportunities

Currently, this project has a lot of assumptions:
-  We assume there's only one validation record
    - We should loop through them, but this involves creating resources inside an `apply`
