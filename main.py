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


def run_spectector(input_file, options=""):
    """
    指定されたファイルに対して spectector を実行する関数。

    Args:
        input_file: 入力ファイルのパス
        options: spectector に渡す追加オプション (例: "-n -a reach")

    Returns:
        subprocess.CompletedProcess: spectector の実行結果
    """
    try:
        # spectector を実行
        spectector_path = "spectector"  # spectector のパス
        # solver = "--nextpath-timeout 100 --noninter-timeout 100 --timeout 5000"  # シェルスクリプトから取得

        command = [spectector_path, input_file] + options.split()
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        return process
    except subprocess.CalledProcessError as e:
        print(f"Error running spectector on {input_file}:")
        print(f"  Return code: {e.returncode}")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return None


def main():
    """
    /tests/spectector_case 内の各ファイルに対して loop_expander を実行し、
    その出力を spectector に入力として与える。
    """
    test_dir = "./tests/sample"  # テストファイルが格納されているディレクトリ

    # /tests/spectector_case 内のファイルをすべて取得
    test_files = glob.glob(os.path.join(test_dir, "*"))

    for test_file in test_files:
        if os.path.isfile(test_file) and test_file.endswith(
            ".muasm"
        ):  # 拡張子 .muasm のファイルのみを対象とする
            print(f"Processing: {test_file}")

            # 1. loop_expander を実行
            loop_expander_result = run_loop_expander(test_file)

            if loop_expander_result:
                # loop_expander の標準出力を一時ファイルに保存
                temp_file = test_file + ".loop_expanded.muasm"
                with open(temp_file, "w") as f:
                    f.write(loop_expander_result.stdout)

                # 2. spectector を実行 (loop_expander の出力を入力として使用)
                print("  Running spectector on expanded code...")
                spectector_result = run_spectector(
                    temp_file
                )  # デフォルトのオプションで実行

                if spectector_result:
                    print(f"  Spectector Stdout:\n{spectector_result.stdout}")
                    if spectector_result.stderr:
                        print(
                            f"  Spectector Warnings/Errors:\n{spectector_result.stderr}"
                        )

                # 3. 必要に応じて concolic testing や non-interference checking を実行
                # 例: concolic testing (reach)
                print("  Running spectector with concolic testing (reach)...")
                spectector_concolic_result = run_spectector(temp_file, "-n -a reach")

                if spectector_concolic_result:
                    print(
                        f"  Spectector (Concolic) Stdout:\n{spectector_concolic_result.stdout}"
                    )
                    if spectector_concolic_result.stderr:
                        print(
                            f"  Spectector (Concolic) Warnings/Errors:\n{spectector_concolic_result.stderr}"
                        )

                # 一時ファイルを削除
                os.remove(temp_file)


if __name__ == "__main__":
    main()
