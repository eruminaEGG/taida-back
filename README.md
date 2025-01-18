## 初期セットアップ

1. 仮想環境用のセットアップ

```shell
/opt/homebrew/bin/python3.11 -m venv venv
python --version #でバージョン確認しても OK
```

2. 仮想環境を実行する

```shell
source venv/bin/activate
```

3. 各モジュールをインストール

```shell
pip install -r requirements.txt
```

4. 【任意】仮想環境を終了

```shell
deactivate
```

## 初回デプロイ手順

1. Google Cloud Platform(GCP) で認証情報の設定を行う  
   https://console.cloud.google.com

2. 後述するデプロイコマンドで AWS のデプロイを行う

3. 生成された情報を GCP の認証情報の設定に追加する  
   API Gateway を開き、認証用のコールバック関数の URL を設定

## デプロイ

```shell
export GOOGLE_CALLBACK_URL="https://example.com"
export GOOGLE_LOGOUT_URL="http://example.com"
export GOOGLE_CLIENT_SECRET=""
export GOOGLE_CLIENT_ID=""
./deploy.sh -a "AWS アクセスキー" -b "AWS シークレットキー" -s "dev"
```
