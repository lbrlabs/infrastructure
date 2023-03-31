import json
import pulumi
import pulumi_aws as aws
import pulumi_github as github

stack_name = pulumi.get_stack()

# create an OIDC provider
github_oidc_provider = aws.iam.OpenIdConnectProvider(
    "github",
    thumbprint_lists=["6938fd4d98bab03faadb97b34396831e3780aea1"],
    client_id_lists=["sts.amazonaws.com", "https://github.com/lbrlabs"],
    url="https://token.actions.githubusercontent.com",
)

# create a dedicated role for GitHub Actions
github_role = aws.iam.Role(
    "github-actions",
    description="Used for Pulumi continuous delivery via GitHub Actions",
    assume_role_policy=github_oidc_provider.arn.apply(
        lambda arn: json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": ["sts:AssumeRoleWithWebIdentity"],
                        "Effect": "Allow",
                        "Condition": {
                            "ForAllValues:StringLike": {
                                "token.actions.githubusercontent.com:sub": "repo:lbrlabs/*"  # allow access from all my repos
                            }
                        },
                        "Principal": {"Federated": [arn]},
                    }
                ],
            }
        )
    ),
    managed_policy_arns=[
        aws.iam.ManagedPolicy.ADMINISTRATOR_ACCESS, # pulumi will likely always need full access
    ]
)

# set the role name as a github secret
secret = github.ActionsOrganizationSecret(
    "role_name",
    secret_name=f"aws_oidc_{stack_name}_role_arn",
    plaintext_value=github_role.arn,
    visibility="all"
)

pulumi_deploy_oidc_provider = aws.iam.OpenIdConnectProvider(
    "pulumi-deploy",
    thumbprint_lists=["9e99a48a9960b14926bb7f3b02e22da2b0ab7280"],
    client_id_lists=["lbrlabs", "sts.amazonaws.com"],
    url="https://api.pulumi.com/oidc",
)

pulumi_role = aws.iam.Role(
    "pulumi-deploy",
    description="Used for Pulumi continuous delivery via Pulumi Deploy",
    assume_role_policy=pulumi_deploy_oidc_provider.arn.apply(
        lambda arn: json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": ["sts:AssumeRoleWithWebIdentity"],
                        "Effect": "Allow",
                        "Condition": {
                            "ForAllValues:StringLike": {
                                "api.pulumi.com/oidc:aud": "lbrlabs",
                                "api.pulumi.com/oidc:sub": "pulumi:deploy:org:lbrlabs:project:*:*"
                            }
                        },
                        "Principal": {"Federated": [arn]},
                    }
                ],
            }
        )
    ),
    managed_policy_arns=[
        aws.iam.ManagedPolicy.ADMINISTRATOR_ACCESS, # pulumi will likely always need full access
    ],
    opts=pulumi.ResourceOptions(delete_before_replace=True)
)

pulumi.export("pulumi_role", pulumi_role.arn)

