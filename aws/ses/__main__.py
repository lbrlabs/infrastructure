import pulumi
import pulumi_aws as aws

config = pulumi.Config()
enabled = config.get_bool("enabled") or False

if enabled:
    domain = aws.ses.DomainIdentity(
        "brig.gs",
        domain="brig.gs",
    )

else:
    pulumi.log.info("SES is disabled in this environment")
    
    
