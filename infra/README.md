# AWS 自動部署（每種節奏一個 branch）

| branch | 頁面 | 網址路徑 |
|---|---|---|
| `jpop` | `pages/jpop.html` | `/jpop/` |
| `rnb` | `pages/rnb.html` | `/rnb/` |
| `rap` | `pages/rap.html` | `/rap/` |
| `pop` | `pages/pop.html` | `/pop/` |
| `full-song` | `pages/full-song.html` | `/full-song/` |

push 到某個 branch，GitHub Actions 只會把那一頁上傳到 `s3://<bucket>/<branch>/index.html`，互不影響。
也可以在 Actions 頁手動按 **Run workflow**（選 branch）。AWS 還沒設定好時 workflow 只會顯示警告並跳過。
之後整合時，再把各 branch 合併回 `main`，改成一次部署整個網站。

## 一次性設定
1. 執行 `BUCKET=<全域唯一名稱> REGION=ap-northeast-1 ./infra/setup-aws.sh`（需要 AWS CLI 與管理員權限）。
2. 依照腳本最後印出的值，在 GitHub repo 的 Settings → Secrets and variables → Actions 新增：
   - Secret `AWS_ROLE_ARN`
   - Variables `S3_BUCKET`、`AWS_REGION`
3. 到 Actions 對每個 branch 手動跑一次 **Deploy rhythm page to S3**。

用 GitHub OIDC 取得臨時憑證，不需要在 GitHub 存 AWS 金鑰；IAM role 只允許本 repo 上面這幾個 branch、只能寫這個 bucket。
新增 branch 時，要同時改 workflow 的 branch 清單與 `Pick page`，並用 `BRANCHES=...` 重跑腳本的 role 部分（或手動更新 trust policy）。

網址為 HTTP（S3 website endpoint）。之後要 HTTPS 可再加 CloudFront。
