#!/usr/bin/env bash
#
# Finishes the kptravel.in deploy: CloudFront + HTTPS + the apex/www DNS records.
#
# Everything else is already provisioned (hosted zone, S3 website bucket, the
# uploaded site, and the ACM request with its validation records). The only
# thing this script waits on is the certificate, and the certificate cannot
# validate until kptravel.in is delegated to Route 53 at GoDaddy:
#
#   ns-378.awsdns-47.com
#   ns-978.awsdns-58.net
#   ns-1473.awsdns-56.org
#   ns-1766.awsdns-28.co.uk
#
# Safe to re-run — it reuses an existing distribution instead of making a second one.
#
# Usage: AWS_PROFILE=kptravel ./deploy/finish-cdn.sh

set -euo pipefail

DOMAIN="kptravel.in"
BUCKET="kptravel.in"
REGION="ap-south-1"
ZONE_ID="Z0814526294QZQL5QNNIE"
CERT_ARN="arn:aws:acm:us-east-1:661842320634:certificate/c2a24ca9-fc23-4d4b-9fe3-984b69c5eb8c"
ORIGIN="${BUCKET}.s3-website.${REGION}.amazonaws.com"

echo "==> Checking certificate status"
STATUS=$(aws acm describe-certificate --region us-east-1 \
  --certificate-arn "$CERT_ARN" \
  --query 'Certificate.Status' --output text)

if [ "$STATUS" != "ISSUED" ]; then
  echo "Certificate is $STATUS, not ISSUED."
  echo
  echo "ACM validates over public DNS, so this stays PENDING_VALIDATION until"
  echo "kptravel.in is delegated to the Route 53 nameservers listed above."
  echo "Check the current delegation with:  dig +short NS kptravel.in"
  exit 1
fi
echo "Certificate is ISSUED."

echo "==> Looking for an existing distribution"
DIST_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?contains(Aliases.Items, '${DOMAIN}')].Id | [0]" \
  --output text)

if [ -n "$DIST_ID" ] && [ "$DIST_ID" != "None" ]; then
  echo "Reusing distribution $DIST_ID"
else
  echo "==> Creating the CloudFront distribution"
  # S3 website endpoints are custom origins, not S3 origins: they speak HTTP
  # only, so the origin protocol policy must be http-only.
  DIST_ID=$(aws cloudfront create-distribution --distribution-config "{
    \"CallerReference\": \"${DOMAIN}-$(date +%s)\",
    \"Comment\": \"KP Travels Solutions Pvt. Ltd. website\",
    \"Enabled\": true,
    \"Aliases\": {\"Quantity\": 2, \"Items\": [\"${DOMAIN}\", \"www.${DOMAIN}\"]},
    \"DefaultRootObject\": \"index.html\",
    \"PriceClass\": \"PriceClass_200\",
    \"Origins\": {
      \"Quantity\": 1,
      \"Items\": [{
        \"Id\": \"s3-website\",
        \"DomainName\": \"${ORIGIN}\",
        \"CustomOriginConfig\": {
          \"HTTPPort\": 80,
          \"HTTPSPort\": 443,
          \"OriginProtocolPolicy\": \"http-only\",
          \"OriginSslProtocols\": {\"Quantity\": 1, \"Items\": [\"TLSv1.2\"]}
        }
      }]
    },
    \"DefaultCacheBehavior\": {
      \"TargetOriginId\": \"s3-website\",
      \"ViewerProtocolPolicy\": \"redirect-to-https\",
      \"Compress\": true,
      \"AllowedMethods\": {
        \"Quantity\": 2,
        \"Items\": [\"GET\", \"HEAD\"],
        \"CachedMethods\": {\"Quantity\": 2, \"Items\": [\"GET\", \"HEAD\"]}
      },
      \"CachePolicyId\": \"658327ea-f89d-4fab-a63d-7e88639e58f6\"
    },
    \"ViewerCertificate\": {
      \"ACMCertificateArn\": \"${CERT_ARN}\",
      \"SSLSupportMethod\": \"sni-only\",
      \"MinimumProtocolVersion\": \"TLSv1.2_2021\"
    }
  }" --query 'Distribution.Id' --output text)
  echo "Created $DIST_ID"
fi

CF_DOMAIN=$(aws cloudfront get-distribution --id "$DIST_ID" \
  --query 'Distribution.DomainName' --output text)
echo "Distribution domain: $CF_DOMAIN"

echo "==> Pointing ${DOMAIN} and www at the distribution"
# Z2FDTNDATAQYW2 is the fixed hosted-zone ID for all CloudFront distributions.
aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" --change-batch "{
  \"Changes\": [
    {\"Action\": \"UPSERT\", \"ResourceRecordSet\": {
      \"Name\": \"${DOMAIN}.\", \"Type\": \"A\",
      \"AliasTarget\": {\"HostedZoneId\": \"Z2FDTNDATAQYW2\", \"DNSName\": \"${CF_DOMAIN}\", \"EvaluateTargetHealth\": false}
    }},
    {\"Action\": \"UPSERT\", \"ResourceRecordSet\": {
      \"Name\": \"www.${DOMAIN}.\", \"Type\": \"A\",
      \"AliasTarget\": {\"HostedZoneId\": \"Z2FDTNDATAQYW2\", \"DNSName\": \"${CF_DOMAIN}\", \"EvaluateTargetHealth\": false}
    }}
  ]
}" --query 'ChangeInfo.Status' --output text

echo
echo "Done. CloudFront takes ~10-15 minutes to reach Deployed:"
echo "  aws cloudfront wait distribution-deployed --id ${DIST_ID}"
echo "Then: https://${DOMAIN}"
