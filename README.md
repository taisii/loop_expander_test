# 論文タイトル

このリポジトリは、論文「[論文タイトル]」で提案されている、ループ展開アルゴリズムと SPECTECTOR を統合した SNI 脆弱性検出システムのソースコードとテスト環境を提供します。

## 構成

- `loop_expander/`: ループ展開アルゴリズム (Go 言語)。[リポジトリURL] の Git Submodule として含まれています。
- `SPECTECTOR/`: SNI 脆弱性検出ツール SPECTECTOR。 [リポジトリURL] の Git Submodule として含まれています。
- `testcases/`: テストケース集。
- `scripts/`: テスト実行スクリプト。
- `LICENSE`: 本リポジトリのライセンス (例: Apache License 2.0)。

## 環境構築とテストの実行方法

1.  このリポジトリをクローンします。
    ```bash
    git clone --recursive [https://github.com/your/repo.git](https://github.com/your/repo.git)
    ```
    `--recursive` オプションを忘れると、Submodule が空になります。その場合は、以下のコマンドで Submodule を初期化・更新してください。
    ```bash
    cd repo
    git submodule update --init --recursive
    ```

2.  `loop_expander` と `SPECTECTOR` は、それぞれのリポジトリの指示に従ってビルドしてください。
    *   `loop_expander`: [loop_expander のリポジトリの README へのリンク]
    *   `SPECTECTOR`: [SPECTECTOR のリポジトリの README へのリンク]

3.  `scripts/run_tests.sh` を実行して、テストを実行します。
    ```bash
    cd scripts
    ./run_tests.sh
    ```

## ライセンス

- 本リポジトリのコード（`loop_expander` と `SPECTECTOR` を除く）は、[あなたのライセンス、例: MIT License] でライセンスされています。
- `loop_expander` は、[loop_expander のライセンス] でライセンスされています。詳細は `loop_expander/LICENSE` をご覧ください。
- `SPECTECTOR` は、Apache License 2.0 でライセンスされています。詳細は `SPECTECTOR/LICENSE` をご覧ください。

## 連絡先

[あなたの名前] <[あなたのメールアドレス]>