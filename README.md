## フォルダ構造
```
- project_root/
  |- Dockerfile
  |- docker-compose.yaml
  |- nginx/
  |  |- nginx.conf
  |- src/
  |  |- manage.py
  |  |- ...
```

## コンテナ作成手順
1. GitHubからソースコードをクローン及びフォルダ名をsrcに変更
```
git clone your_github_repo_url src
```

2. Dockerコンテナをビルドと起動
```
docker-compose up --build -d
```

アプリケーションは http://localhost/ でアクセス可能
phpMyAdminは http://localhost:8080/ でアクセス可能

## gitingnoreの作成
キャッシュファイルをgit管理から外します。
1. ルートディレクトリ（Dockerfileがあるディレクトリ）に.gitignoreファイルを作成します。
2. 以下を記述して保存する。 
```
.gitignore
*.pyc
```

## Sassの設定方法
1. プロジェクト直下にstatic/アプリ名/cssディレクトリを作成する
2. VSCodeの拡張でLive Sass Compilerをインストール
3. LiveSassCompilerの設定画面からFormatsをsettings.jsonで開く
4. savePathのディレクトリでcssファイルの出力先を指定する。（ルートは現在開いているディレクトリが基点）
```json
"savePath": "/src/【プロジェクト名】/static/【アプリ名】/css",
例）
"savePath": "/src/TeamA/static/dialy/css",
```
5. cssディレクトリやscssディレクトリにstyle.scssを作成し、cssを記述する
6. 画面右下のwatchsassボタンをクリックするとリアルタイムでコンパイルして指定フォルダへ出力される。

## サーバーサイドの編集について
※サーバーを再起動しないと反映されません。
```bash
docker compose restart web
```
3秒かからず再起動が完了し、反映されます。

## フロントエンドの編集について
※nginxに静的ファイルを送らないと反映されません。
1. コンテナ内に入ります。
```bash
docker exec -it django_gunicorn /bin/bash
```
2. collectstaticコマンドでnginxに静的ファイルを送ります。
```bash
python manage.py collectstatic --noinput
```
※即時反映されます。shift + F5でスーパーリロードしてください。