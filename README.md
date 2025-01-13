# 論文タイトル

このリポジトリは、論文「[SNI 検出アルゴリズムへの単純ループへの拡張]」で提案されている、ループ展開アルゴリズムと SPECTECTOR を統合した SNI 検出システムのテスト環境を提供します。

## 構成

- `testcases/`: テストケース集。SPECTECTOR のレポジトリから取ってきたものと自作のものが含まれます。
- `main.py`: テスト実行スクリプト。

## 環境構築とテストの実行方法

1.  このリポジトリをクローンします。

    ```bash
    git@github.com:taisii/loop_expander_test.git
    ```

2.  `loop_expander` と `SPECTECTOR` をそれぞれのリポジトリの指示に従ってクローン及びビルドしてください。

    - `loop_expander`: https://github.com/spectector/spectector
    - `SPECTECTOR`: https://github.com/taisii/loop_expander

3.  `main.py` を実行して、テストを実行します。
    ```bash
    python3 main.py
    ```
