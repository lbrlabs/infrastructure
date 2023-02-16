import json
import pulumi
import pulumi_aws as aws
import pulumi_github as github

stack_name = pulumi.get_stack()

# create an OIDC provider
oidc_provider = aws.iam.OpenIdConnectProvider(
    "github",
    thumbprint_lists=["6938fd4d98bab03faadb97b34396831e3780aea1"],
    client_id_lists=["sts.amazonaws.com", "https://github.com/jaxxstorm"],
    url="https://token.actions.githubusercontent.com",
)

# create a dedicated role for GitHub Actions
role = aws.iam.Role(
    "github-actions",
    description="Used for Pulumi continuous delivery via GitHub Actions",
    assume_role_policy=oidc_provider.arn.apply(
        lambda arn: json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": ["sts:AssumeRoleWithWebIdentity"],
                        "Effect": "Allow",
                        "Condition": {
                            "ForAllValues:StringLike": {
                                "token.actions.githubusercontent.com:sub": "repo:jaxxstorm/*"  # allow access from all my repos
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

# # set the role name as a github secret
# secret = github.ActionsOrganizationSecret(
#     "role_name",
#     secret_name=f"aws_oidc_{stack_name}_role_arn",
#     plaintext_value=role.arn,
#     visibility="all"
# )

secret = github.ActionsSecret(
    "role_name",
    secret_name=f"aws_oidc_{stack_name}_role_arn",
    plaintext_value=role.arn,
    repository="lbrlabs",
)