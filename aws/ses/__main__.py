import pulumi
import pulumi_aws as aws
import pulumi_cloudflare as cloudflare

config = pulumi.Config()
domains = config.require_object("domains")

for domain in domains:
    domain_identity = aws.ses.DomainIdentity(
        domain,
        domain=domain,
    )

    zone = cloudflare.get_zone_output(name=domain)

    record = cloudflare.Record(
        f"{domain}-verification",
        name="_amazonses." + domain,
        zone_id=zone.id,
        value=domain_identity.verification_token,
        ttl=60,
        type="TXT",
        proxied=False,
        opts=pulumi.ResourceOptions(delete_before_replace=True),
    )

    verification = aws.ses.DomainIdentityVerification(
        domain,
        domain=domain_identity.domain,
        opts=pulumi.ResourceOptions(depends_on=[record]),
    )
    
    mail_from = aws.ses.MailFrom(
        domain,
        domain=domain_identity.domain,
        mail_from_domain=pulumi.Output.concat("mail."+domain),
    )
    
    mx_record = cloudflare.Record(
        f"{domain}-mx",
        name=pulumi.Output.concat("mail."+domain),
        zone_id=zone.id,
        type="MX",
        ttl=600,
        priority=10,
        value="feedback-smtp.us-west-2.amazonses.com",
    )
    
    txt_record = cloudflare.Record(
        f"{domain}-txt",
        name=pulumi.Output.concat("mail."+domain),
        zone_id=zone.id,
        type="TXT",
        ttl=60,
        value="v=spf1 include:amazonses.com ~all",
    )
    
    
