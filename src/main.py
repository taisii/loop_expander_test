import glob
import logging
import os
import time
from loop_expander import run_loop_expander
from metrics import save_metrics
from spectector import run_spectector, save_spectector_output

timeout = 2


def process_single_file(
    test_file, algorithm, loop_expansion_limit=3, spectector_options=""
) -> dict[str, any]:
    """
    単一の .muasm ファイルを処理する関数。

    Args:
        test_file: 処理する .muasm ファイルのパス
        algorithm: 実行するアルゴリズム ("proposed" or "baseline")
        loop_expansion_limit: ループの展開回数の上限 (提案手法の場合)
        spectector_options: spectector に渡す追加オプション

    Returns:
        metrics: 収集したメトリクス
    """
    logging.info(f"Processing: {test_file} (algorithm: {algorithm})")

    metrics = {
        "execution_time": 0.0,
        "loop_expander_time": 0.0,
        "spectector_time": 0.0,
        "leak": False,
        "successful": False,
        "timeout": False,
    }

    start_time = time.time()

    try:
        if algorithm == "proposed":
            temp_file = test_file + ".loop_expanded.muasm"

            loop_expander_start_time = time.time()
            loop_expander_success = run_loop_expander(
                test_file, temp_file, loop_expansion_limit
            )
            metrics["loop_expander_time"] = time.time() - loop_expander_start_time

            if not loop_expander_success:
                logging.error("Loop expansion failed.")
                return metrics

            logging.info("  Running spectector on expanded code...")
            spectector_result = run_spectector(temp_file, timeout, spectector_options)
            metrics["spectector_time"] = spectector_result.execution_time

            if spectector_result.timeout:
                logging.warning("Spectector timed out!")
                metrics["timeout"] = True
                return metrics

            if spectector_result.returncode != 0:
                logging.error(
                    f"Spectector returned non-zero exit code: {spectector_result.returncode}"
                )
                logging.error(f"Spectector stderr:\n{spectector_result.stderr}")
                return metrics

            if spectector_result.stdout:
                save_spectector_output(
                    test_file, spectector_result, algorithm, loop_expansion_limit
                )
                # spectector_metrics = parse_spectector_output(spectector_result.stdout)
                # metrics.update(spectector_metrics)
                metrics["successful"] = True

            os.remove(temp_file)

        elif algorithm == "baseline":
            logging.info("  Running spectector on original code...")
            spectector_result = run_spectector(test_file, timeout, spectector_options)
            metrics["spectector_time"] = spectector_result.execution_time

            if spectector_result.timeout:
                logging.warning("Spectector timed out!")
                metrics["timeout"] = True
                return metrics

            if spectector_result.returncode != 0:
                logging.error(
                    f"Spectector returned non-zero exit code: {spectector_result.returncode}"
                )
                logging.error(f"Spectector stderr:\n{spectector_result.stderr}")
                return metrics

            if spectector_result.stdout:
                save_spectector_output(test_file, spectector_result, algorithm)
                # spectector_metrics = parse_spectector_output(spectector_result.stdout)
                # metrics.update(spectector_metrics)
                metrics["successful"] = True

        else:
            logging.error(f"Error: Unknown algorithm: {algorithm}")
            return metrics

        metrics["execution_time"] = time.time() - start_time

    except Exception as e:
        logging.error(f"Error during processing: {e}")

    return metrics


def main():
    """
    /tests/sample 内の各 .muasm ファイルに対して、
    process_single_file 関数を適用する。
    """
    test_dir = "./../tests/sample"  # テストファイルが格納されているディレクトリ

    # /tests/sample 内の .muasm ファイルをすべて取得
    test_files = glob.glob(os.path.join(test_dir, "*.muasm"))

    for test_file in test_files:
        metrics = process_single_file(test_file, "baseline")
        save_metrics(metrics, test_file, "baseline")


if __name__ == "__main__":
    main()
