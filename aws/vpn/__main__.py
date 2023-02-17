import pulumi
import lbrlabs_pulumi_tailscalebastion as tailscale

awsconfig = pulumi.Config("aws")
region = awsconfig.require("region")

config = pulumi.Config()
org = config.require("org")

stack = pulumi.get_stack()

vpc = pulumi.StackReference(f"{org}/aws_vpc/{stack}")
vpc_id = vpc.require_output("vpc_id")
subnet_ids = vpc.require_output("private_subnet_ids")
cidr_block = vpc.require_output("cidr_block")

bastion = tailscale.aws.Bastion(
    "tailscale-vpn",
    vpc_id=vpc_id,
    subnet_ids=subnet_ids,
    route=cidr_block,
    region=region
)

pulumi.export("ssh_key", bastion.private_key)