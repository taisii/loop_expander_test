import subprocess
import os
import glob


def run_loop_expander(input_file):
    """
    指定されたファイルに対して loop_expander を実行する関数。

    Args:
        input_file: 入力ファイルのパス

    Returns:
        subprocess.CompletedProcess: loop_expander の実行結果
    """
    try:
        # loop_expander を実行
        process = subprocess.run(
            ["./loop_expander/go-project", "-i", os.path.abspath(input_file)],
            capture_output=True,
            text=True,
            check=True,  # エラー時に例外を発生させる
        )
        return process
    except subprocess.CalledProcessError as e:
        print(f"Error running loop_expander on {input_file}:")
        print(f"  Return code: {e.returncode}")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return None


def main():
    """
    /tests/spectector_case 内の各ファイルに対して loop_expander を実行する。
    """
    test_dir = "./tests/spectector_case"  # テストファイルが格納されているディレクトリ

    # /tests/spectector_case 内のファイルをすべて取得
    # (サブディレクトリも再帰的に探索する場合)
    # test_files = glob.glob(os.path.join(test_dir, "**/*"), recursive=True)
    # (サブディレクトリは探索しない場合)
    test_files = glob.glob(os.path.join(test_dir, "*"))

    for test_file in test_files:
        if os.path.isfile(test_file):
            print(f"Processing: {test_file}")
            result = run_loop_expander(test_file)

            if result:
                # loop_expander の実行結果を処理
                # 標準出力の内容を表示
                print(f"  Stdout:\n{result.stdout}")
                # # 例: 標準出力をファイルに保存
                # output_file = test_file + ".out"
                # with open(output_file, "w") as f:
                #     f.write(result.stdout)

                # 例: 標準エラー出力がある場合、エラーメッセージを表示
                if result.stderr:
                    print(f"  Warnings/Errors:\n{result.stderr}")
                # else:
                #     print(
                #         f"  loop_expander ran successfully. Output written to {output_file}"
                #     )


if __name__ == "__main__":
    main()
