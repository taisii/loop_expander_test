#!/bin/bash

# Ciao をインストール
curl https://ciao-lang.org/boot -sSfL | sh

# SPECTECTORをビルド
export CIAOPATH=/app
# ciao build -r spectector

bash
# main.py を実行
# python3 main.py