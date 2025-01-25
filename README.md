# Loop_expander_test

このリポジトリは、論文「SNI 検出アルゴリズムへの単純ループへの拡張」で提案されている、ループ展開アルゴリズムと SPECTECTOR を統合した SNI 検出システムのテスト環境を提供します。

## 構成

- `testcases/`: テストケース集。
- `src/`: テスト実行スクリプト群。
- `run.sh`: ビルドとテストの実行を行うためのスクリプト

## 環境構築とテストの実行方法

1.  Ciao, Go, Python を実行できる環境を作成してください。

    Ciao の環境構築については[公式サイト](https://ciao-lang.org/ciao/build/doc/ciao.html/Install.html#Checking%20for%20correct%20installation)を参考にしてください。

2.  このリポジトリをクローンします。

    ```bash
    git pull -r git@github.com:taisii/loop_expander_test.git
    ```

3.  `run.sh` を実行して、テストを実行します。
    ```bash
    ./run.sh
    ```
