"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

stack_name = pulumi.get_stack()
config = pulumi.Config()
aws_config = pulumi.Config("aws")
insights_enabled = config.get_bool("enable_insights") or False
log_retention = config.get("log_retention") or 7
region = aws_config.require("region")

"""
We'll use the account id for some policy documents
"""
account = aws.get_caller_identity()

""" create a KMS key for encrypting logs """
key = aws.kms.Key(
    f"ecs-log-key-{stack_name}",
    description="Used to encrypt ECS cluster logs",
    deletion_window_in_days=28,
    enable_key_rotation=True,
    policy=aws.iam.get_policy_document(
        statements=[
            aws.iam.GetPolicyDocumentStatementArgs(
                sid="Allow IAM user access",
                actions=["kms:*"],
                effect="Allow",
                resources=["*"],
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="AWS", identifiers=[f"arn:aws:iam::{account.account_id}:root"]
                )],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                sid="Allow Cloudwatch Logs access",
                actions=["kms:Encrypt*", "kms:Decrypt*", "kms:ReEncrypt*", "kms:GenerateDataKey*", "kms:DescribeKey"],
                effect="Allow",
                resources=["*"],
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="Service", identifiers=[f"logs.{region}.amazonaws.com"]
                )]
            )
        ]
    ).json,
)

""" encrypt the log group with the KMS key """
log_group = aws.cloudwatch.LogGroup(
    f"ecs-log-group-{stack_name}",
    kms_key_id=key.arn,
    retention_in_days=log_retention,
)

""" container insights are important in prod
but are expensive, so we need to make them configurable """
if insights_enabled:
    pulumi.log.debug("enabling container insights")
    cluster_settings = aws.ecs.ClusterSettingArgs(
        name="containerInsights",
        value="enabled",
    )
else:
    cluster_settings = None

cluster = aws.ecs.Cluster(
    f"ecs-{stack_name}",
    settings=[cluster_settings],
    configuration=aws.ecs.ClusterConfigurationArgs(
        execute_command_configuration=aws.ecs.ClusterConfigurationExecuteCommandConfigurationArgs(
            kms_key_id=key.arn,
            logging="OVERRIDE",
            log_configuration=aws.ecs.ClusterConfigurationExecuteCommandConfigurationLogConfigurationArgs(
                cloud_watch_encryption_enabled=True,
                cloud_watch_log_group_name=log_group.name,
            ),
        )
    ),
)

aws.ecs.ClusterCapacityProviders(
    f"ecs-capacity-provider-{stack_name}",
    cluster_name=cluster.name,
    capacity_providers=["FARGATE", "FARGATE_SPOT"],
    default_capacity_provider_strategies=[
        aws.ecs.ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs(
            base=1, weight=100, capacity_provider="FARGATE_SPOT"
        )
    ],
    opts=pulumi.ResourceOptions(parent=cluster),
)


pulumi.export("cluster_name", cluster.name)
pulumi.export("cluster_arn", cluster.arn)