import pulumi
import lbrlabs_pulumi_tailscalebastion as tailscale

config = pulumi.Config("aws")
region = config.require("region")

stack = pulumi.get_stack()

vpc = pulumi.StackReference(f"jaxxstorm/vpc/{stack}")
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