import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const cert = new aws.acm.Certificate("wilcard", {
    domainName: "*.aws.lbrlabs.com",
    validationMethod: "DNS",
})

const domain = aws.route53.getZoneOutput({
    name: "aws.lbrlabs.com",
    privateZone: false,
});

// we assume there's only one validation record
const validationRecord = new aws.route53.Record("wildcard", {
    name: cert.domainValidationOptions[0].resourceRecordName,
    records: [ cert.domainValidationOptions[0].resourceRecordValue ],
    type: cert.domainValidationOptions[0].resourceRecordType,
    zoneId: domain.id,
    ttl: 60
})

// const records: aws.route53.Record[] = [];

// cert.domainValidationOptions.apply(options => {
//     options.forEach(option => {
//         const record = new aws.route53.Record(option.domainName, {
//             name: option.resourceRecordName,
//             records: [ option.resourceRecordValue ],
//             type: option.resourceRecordType,
//             zoneId: domain.id,
//         })
//         records.push(record)

//     })
// })

const certValidation = new aws.acm.CertificateValidation("wildcard", {
    certificateArn: cert.arn,
    validationRecordFqdns: [ validationRecord.fqdn ],
}, { parent: cert });

