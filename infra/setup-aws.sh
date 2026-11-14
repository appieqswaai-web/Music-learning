#!/usr/bin/env bash
# One-time AWS setup for the J-pop page static site.
# Creates: a public S3 static-website bucket, a GitHub OIDC provider (if missing),
# and an IAM role that only this repo's page branches can assume, allowed to write to the bucket.
# Usage: BUCKET=my-unique-name REGION=ap-northeast-1 ./infra/setup-aws.sh
set -euo pipefail
BUCKET="${BUCKET:?set BUCKET}"
REGION="${REGION:-ap-northeast-1}"
REPO="${REPO:-appieqswaai-web/Music-learning}"
ROLE_NAME="${ROLE_NAME:-music-learning-deploy}"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 1) Bucket as public static website (each page lives under /<branch>/)
aws s3api create-bucket --bucket "$BUCKET" --region "$REGION" \
  --create-bucket-configuration LocationConstraint="$REGION"
aws s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false
aws s3 website "s3://$BUCKET" --index-document index.html
aws s3api put-bucket-policy --bucket "$BUCKET" --policy "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{\"Sid\":\"PublicRead\",\"Effect\":\"Allow\",\"Principal\":\"*\",
    \"Action\":\"s3:GetObject\",\"Resource\":\"arn:aws:s3:::$BUCKET/*\"}]}"

# 2) GitHub OIDC provider (skip if it already exists)
PROVIDER_ARN="arn:aws:iam::$ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
aws iam get-open-id-connect-provider --open-id-connect-provider-arn "$PROVIDER_ARN" >/dev/null 2>&1 || \
  aws iam create-open-id-connect-provider --url https://token.actions.githubusercontent.com \
    --client-id-list sts.amazonaws.com

# 3) Deploy role: only the page branches of this repo, only this bucket
BRANCHES="${BRANCHES:-jpop rnb rap pop full-song}"
SUBS=$(for b in $BRANCHES; do printf '\"repo:%s:ref:refs/heads/%s\",' "$REPO" "$b"; done | sed 's/,$//')
aws iam create-role --role-name "$ROLE_NAME" --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Federated\":\"$PROVIDER_ARN\"},
    \"Action\":\"sts:AssumeRoleWithWebIdentity\",
    \"Condition\":{
      \"StringEquals\":{\"token.actions.githubusercontent.com:aud\":\"sts.amazonaws.com\"},
      \"StringLike\":{\"token.actions.githubusercontent.com:sub\":[$SUBS]}}}]}"
aws iam put-role-policy --role-name "$ROLE_NAME" --policy-name s3-deploy --policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[
    {\"Effect\":\"Allow\",\"Action\":[\"s3:PutObject\",\"s3:DeleteObject\"],\"Resource\":\"arn:aws:s3:::$BUCKET/*\"},
    {\"Effect\":\"Allow\",\"Action\":\"s3:ListBucket\",\"Resource\":\"arn:aws:s3:::$BUCKET\"}]}"

echo
echo "Done. In GitHub repo Settings > Secrets and variables > Actions:"
echo "  secret   AWS_ROLE_ARN = arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME"
echo "  variable S3_BUCKET    = $BUCKET"
echo "  variable AWS_REGION   = $REGION"
echo "Pages: http://$BUCKET.s3-website-$REGION.amazonaws.com/<branch>/  (branches: $BRANCHES)"
