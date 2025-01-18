#!/bin/bash

# spectector と loop_expander をビルド
ciao build -r spectector
cd loop_expander
go build -o go-project
cd ..

# main.py を実行
python3 main.py