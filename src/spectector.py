import os
import subprocess
import time
import logging


class SpectectorResult:
    def __init__(self, stdout, stderr, returncode, execution_time, timeout=False):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.execution_time = execution_time
        self.timeout = timeout


def run_spectector(input_file, timeout, options=""):
    """
    指定されたファイルに対して spectector を実行する関数。

    Args:
        input_file: 入力ファイルのパス
        timeout: タイムアウト時間 (秒)
        options: spectector に渡す追加オプション (例: "-n -a reach")

    Returns:
        SpectectorResult: spectector の実行結果 (エラー時は None)
    """
    try:
        command = ["spectector", input_file] + options.split()
        start_time = time.time()
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        end_time = time.time()
        return SpectectorResult(
            process.stdout, process.stderr, process.returncode, end_time - start_time
        )

    except subprocess.TimeoutExpired:
        end_time = time.time()
        logging.warning(
            f"Spectector timed out on {input_file} after {timeout} seconds!"
        )
        return SpectectorResult(None, None, None, end_time - start_time, timeout=True)

    except Exception as e:
        end_time = time.time()
        logging.error(f"Error running spectector on {input_file}: {e}")
        return SpectectorResult(None, None, 1, end_time - start_time)


def save_spectector_output(test_file, spectector_result, algorithm, loop_count=None):
    """
    spectector の結果をファイルに保存する関数。

    Args:
        test_file: テストファイルのパス
        spectector_result: spectector の実行結果 (SpectectorResult オブジェクト)
        algorithm: 実行したアルゴリズム ("proposed" or "baseline")
        loop_count: ループの展開回数 (提案手法の場合のみ)
    """
    if algorithm == "proposed":
        output_filename = (
            os.path.splitext(test_file)[0] + f".{algorithm}.{loop_count}.out"
        )
    else:
        output_filename = os.path.splitext(test_file)[0] + f".{algorithm}.out"

    with open(output_filename, "w") as f:
        if spectector_result.stdout:
            f.write("Stdout:\n")
            f.write(spectector_result.stdout)
        else:
            f.write("Stdout: (empty - Spectector likely timed out or had an error)\n")

        if spectector_result.stderr:
            f.write("\nStderr:\n")
            f.write(spectector_result.stderr)
        else:
            f.write("\nStderr: (empty)\n")

        f.write(f"\nReturn Code: {spectector_result.returncode}\n")
        f.write(f"Execution Time: {spectector_result.execution_time} seconds\n")
        if spectector_result.timeout:
            f.write("Timeout: True\n")
        else:
            f.write("Timeout: False\n")

    print(f"  Spectector output saved to: {output_filename}")
