#!/bin/bash

# Ciao をインストール
# curl https://ciao-lang.org/boot -sSfL | sh

# goのモジュールをビルド
cd loop_expander
go build
cd ..

# main.py を実行
python3 main.py