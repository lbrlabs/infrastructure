import * as pulumi from "@pulumi/pulumi";
import * as cloudflare from "@pulumi/cloudflare";

const domain = new cloudflare.Zone("leebriggs.co.uk", {
  zone: "leebriggs.co.uk",
});

new cloudflare.Record("root", {
    name: "leebriggs.co.uk",
    type: "CNAME",
    proxied: true,
    zoneId: domain.id,
    value: "jaxxstorm-github-io.pages.dev"
})

new cloudflare.Record("www.", {
    name: "www",
    type: "CNAME",
    proxied: true,
    zoneId: domain.id,
    value: "jaxxstorm-github-io.pages.dev",
})

new cloudflare.Record("mail-verification-0", {
    name: "leebriggs.co.uk",
    type: "MX",
    value: "aspmx2.googlemail.com",
    priority: 10,
    zoneId: domain.id,
    proxied: false,
})

new cloudflare.Record("mail-verification-1", {
    name: "leebriggs.co.uk",
    type: "MX",
    value: "alt1.aspmx.l.google.com",
    priority: 5,
    zoneId: domain.id,
    proxied: false,
})

new cloudflare.Record("mail-verification-2", {
    name: "leebriggs.co.uk",
    type: "MX",
    value: "aspmx.l.google.com",
    priority: 1,
    zoneId: domain.id,
    proxied: false,
})

new cloudflare.Record("mail-verification-3", {
    name: "leebriggs.co.uk",
    type: "MX",
    value: "alt2.aspmx.l.google.com",
    priority: 10,
    zoneId: domain.id,
    proxied: false,
})


new cloudflare.Record("keybase", {
    name: "leebriggs.co.uk",
    type: "TXT",
    zoneId: domain.id,
    proxied: false,
    value: "keybase-site-verification=CNR0w8Sai4r3Fq2gfbVN9FvgVpuXyYLLDaFKVO9JNgE"
})


