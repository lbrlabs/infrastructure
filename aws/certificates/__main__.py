import pulumi
import pulumi_aws as aws
import pulumi_cloudflare as cloudflare

config = pulumi.Config()
domains = config.require_object("domains")

for domain in domains:
    cert = aws.acm.Certificate(
        domain,
        domain_name=domain,
        subject_alternative_names=[
            f"*.{domain}",
        ],
        validation_method="DNS",
    )

    zone = cloudflare.get_zone_output(name=domain)

    cloudflare.Record(
        domain,
        name=cert.domain_validation_options[0].resource_record_name,
        zone_id=zone.id,
        value=cert.domain_validation_options[0].resource_record_value,
        ttl=60,
        type=cert.domain_validation_options[0].resource_record_type,
        proxied=False,
    )
    pulumi.export(f"{domain}_cert_arn", cert.arn)