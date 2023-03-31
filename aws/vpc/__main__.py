import pulumi
import pulumi_awsx as awsx
import pulumi_aws as aws

config = pulumi.Config()
cidr_block = config.require("cidr_block")
number_of_availability_zones = config.require_int("number_of_availability_zones")
enable_nat_gateway = config.require_bool("enable_nat_gateway")
stack_name = pulumi.get_stack()

if enable_nat_gateway:
    nat_gateway_strategy = awsx.ec2.NatGatewayStrategy.SINGLE
else:
    nat_gateway_strategy = awsx.ec2.NatGatewayStrategy.NONE


vpc = awsx.ec2.Vpc(
    f"vpc-{stack_name}",
    cidr_block=cidr_block,
    subnet_specs=[
        awsx.ec2.SubnetSpecArgs(
            type="public",
        ),
        awsx.ec2.SubnetSpecArgs(
            type="private",
        ),
    ],
    number_of_availability_zones=number_of_availability_zones,
    nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(strategy=nat_gateway_strategy),
)

route_tables = aws.ec2.get_route_tables(
    vpc_id=vpc.vpc_id,
    tags={
        "SubnetType": "Private",
    },
)



pulumi.export("route_table_ids", route_tables)
pulumi.export("vpc_id", vpc.vpc_id)
pulumi.export("public_subnet_ids", vpc.public_subnet_ids)
pulumi.export("private_subnet_ids", vpc.private_subnet_ids)
pulumi.export("cidr_block", cidr_block)