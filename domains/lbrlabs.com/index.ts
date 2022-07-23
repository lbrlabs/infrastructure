import * as pulumi from "@pulumi/pulumi";
import * as cloudflare from "@pulumi/cloudflare";
import * as aws from "@pulumi/aws";

const domain = new cloudflare.Zone("lbrlabs.com", {
  zone: "lbrlabs.com",
});

const subdomain = new aws.route53.Zone("aws.lbrlabs.com", {
    name: "aws.lbrlabs.com"
});

// eugh, inside an apply
subdomain.nameServers.apply(nameservers => {
    nameservers.forEach((nameserver, index) => {
        new cloudflare.Record(`ns-${index}`, {
            name: "aws",
            type: "NS",
            zoneId: domain.id,
            ttl: 300,
            value: nameserver,
            // data: {
            //     content: nameserver
            // },
            proxied: false,
        }, { parent: domain })        
    });

})
