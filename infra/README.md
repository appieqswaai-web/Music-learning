# AWS 自動部署（目前只部署 J-pop 頁）

push 到 `main` 且 `pages/jpop.html` 有改動時，GitHub Actions 會把它上傳到 S3 當作網站首頁 `index.html`。
也可以在 Actions 頁手動按 **Run workflow**。

## 一次性設定
1. 執行 `BUCKET=<全域唯一名稱> REGION=ap-northeast-1 ./infra/setup-aws.sh`（需要 AWS CLI 與管理員權限）。
2. 依照腳本最後印出的值，在 GitHub repo 的 Settings → Secrets and variables → Actions 新增：
   - Secret `AWS_ROLE_ARN`
   - Variables `S3_BUCKET`、`AWS_REGION`
3. 到 Actions 手動跑一次 **Deploy J-pop page to S3**。

用 GitHub OIDC 取得臨時憑證，不需要在 GitHub 存 AWS 金鑰；IAM role 只允許本 repo 的 `main` 分支、只能寫這個 bucket。

網址為 HTTP（S3 website endpoint）。之後要 HTTPS 可再加 CloudFront。
