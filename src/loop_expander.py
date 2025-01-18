import subprocess
import os


def run_loop_expander(
    input_file: str, output_file: str, loop_expansion_limit: int = 3
) -> bool:
    """
    指定されたファイルに対して loop_expander を実行する関数。

    Args:
        input_file: 入力ファイルのパス
        output_file: 出力ファイルのパス
        loop_expansion_limit: ループの展開回数の上限

    Returns:
        bool: loop_expander が正常に終了した場合は True, エラーが発生した場合は False
    """
    try:
        # loop_expander を実行
        subprocess.run(
            [
                "./../loop_expander/go-project",
                "-i",
                os.path.abspath(input_file),
                "-o",
                os.path.abspath(output_file),
                "-n",
                str(loop_expansion_limit),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running loop_expander on {input_file}:")
        print(f"  Return code: {e.returncode}")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return False
