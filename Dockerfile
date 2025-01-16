# ベースイメージとして Ubuntu の最新版を指定
FROM ubuntu:latest

# apt パッケージの情報を更新
RUN apt-get update

# python3 と python3-pip をインストール
RUN apt-get install -y curl python3 python3-pip

# ciao環境をインストール
RUN apt-get install build-essential
RUN apt-get install -y emacs

# Goのインストール
ARG GO_VERSION=1.23.3  # 必要であればバージョンを指定
RUN apt-get install -y golang-go

# 作業ディレクトリを設定
WORKDIR /app
COPY . /app

# run.sh に実行権限を付与
RUN chmod +x ./run.sh

# スクリプトの実行
CMD ["./run.sh"]