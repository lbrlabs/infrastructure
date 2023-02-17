import pulumi
import pulumi_aws as aws

stack = pulumi.get_stack()
config = pulumi.Config()
internal = config.get_bool("internal") or False
org = config.require("org")
domain = config.require("domain")

vpc = pulumi.StackReference(f"{org}/aws_vpc/{stack}")
vpc_id = vpc.require_output("vpc_id")
subnet_ids = vpc.require_output("public_subnet_ids")

cert = pulumi.StackReference(f"{org}/aws_certificates/{stack}")
cert_arn = cert.require_output(f"{domain}_cert_arn")


security_group = aws.ec2.SecurityGroup(
    "shared-loadbalancer-sg",
    description=f"Security group for shared load balancer in {stack}",
    vpc_id=vpc_id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
)

lb = aws.lb.LoadBalancer(
    "shared-lb",
    internal=internal,
    load_balancer_type="application",
    subnets=subnet_ids,
    security_groups=[security_group.id],
)

target_group = aws.lb.TargetGroup(
    "shared-lb-target-group",
    protocol="HTTP",
    target_type="ip",
    vpc_id=vpc_id,
    port=80,
    health_check=aws.lb.TargetGroupHealthCheckArgs(
        matcher="200-302",
    ),
    opts=pulumi.ResourceOptions(parent=lb),
)

http = aws.lb.Listener(
    "shared-lb-http",
    load_balancer_arn=lb.arn,
    port=80,
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="redirect",
            redirect=aws.lb.ListenerDefaultActionRedirectArgs(
                port="443",
                protocol="HTTPS",
                status_code="HTTP_301",
            ),
        )
    ],
    opts=pulumi.ResourceOptions(parent=lb),
)

https = aws.lb.Listener(
    "shared-lb-https",
    load_balancer_arn=lb.arn,
    port=443,
    protocol="HTTPS",
    certificate_arn=cert_arn,
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="forward",
            forward=aws.lb.ListenerDefaultActionForwardArgs(
                target_groups=[
                    aws.lb.ListenerDefaultActionForwardTargetGroupArgs(
                        arn=target_group.arn
                    )
                ]
            ),
        ),
    ],
)

pulumi.export("lb_arn", lb.arn)
pulumi.export("lb_dns_name", lb.dns_name)
pulumi.export("lb_zone_id", lb.zone_id)
pulumi.export("lb_security_group_id", security_group.id)
pulumi.export("http_listener_arn", http.arn)
pulumi.export("target_group_arn", target_group.arn)
