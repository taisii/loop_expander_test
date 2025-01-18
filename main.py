import subprocess
import os
import glob


def run_loop_expander(input_file):
    """
    指定されたファイルに対して loop_expander を実行する関数。

    Args:
        input_file: 入力ファイルのパス

    Returns:
        str: loop_expander の標準出力 (エラー時は None)
    """
    try:
        # loop_expander を実行
        process = subprocess.run(
            ["./loop_expander/go-project", "-i", os.path.abspath(input_file)],
            capture_output=True,
            text=True,
            check=True,  # エラー時に例外を発生させる
        )
        return process.stdout
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
        subprocess.CompletedProcess: spectector の実行結果 (エラー時は None)
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


def save_spectector_output(test_file, spectector_result):
    """
    spectector の結果をファイルに保存する関数。

    Args:
        test_file: テストファイルのパス
        spectector_result: spectector の実行結果 (subprocess.CompletedProcess)
    """
    output_filename = os.path.splitext(test_file)[0] + ".out"
    with open(output_filename, "w") as f:
        f.write("Stdout:\n")
        f.write(spectector_result.stdout)
        if spectector_result.stderr:
            f.write("\nStderr:\n")
            f.write(spectector_result.stderr)
    print(f"  Spectector output saved to: {output_filename}")


def process_single_file(test_file):
    """
    単一の .muasm ファイルを処理する関数。
    loop_expander を実行し、その結果を spectector に渡す。

    Args:
        test_file: 処理する .muasm ファイルのパス
    """
    print(f"Processing: {test_file}")

    # 1. loop_expander を実行
    loop_expander_output = run_loop_expander(test_file)

    if loop_expander_output:
        # loop_expander の標準出力を一時ファイルに保存
        temp_file = test_file + ".loop_expanded.muasm"
        with open(temp_file, "w") as f:
            f.write(loop_expander_output)

        # 2. spectector を実行 (loop_expander の出力を入力として使用)
        print("  Running spectector on expanded code...")
        spectector_result = run_spectector(temp_file)  # デフォルトのオプションで実行

        if spectector_result:
            # 結果をファイルに保存
            save_spectector_output(test_file, spectector_result)

        # 一時ファイルを削除
        os.remove(temp_file)


def main():
    """
    /tests/sample 内の各 .muasm ファイルに対して、
    process_single_file 関数を適用する。
    """
    test_dir = "./tests/sample"  # テストファイルが格納されているディレクトリ

    # /tests/sample 内の .muasm ファイルをすべて取得
    test_files = glob.glob(os.path.join(test_dir, "*.muasm"))

    for test_file in test_files:
        process_single_file(test_file)


if __name__ == "__main__":
    main()
