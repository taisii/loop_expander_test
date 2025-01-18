import glob
import logging
import os
import time

import pandas as pd
from loop_expander import run_loop_expander
from metrics import analyze_spectector_result, compare_and_store_metrics, compare_metrics, save_metrics
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
                analyze_spectector_result(spectector_result, metrics)

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
                analyze_spectector_result(spectector_result, metrics)

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
    test_dir = "./../tests"  # テストファイルが格納されているディレクトリ

    # 結果を格納するDataFrameを作成
    results_df = pd.DataFrame()

    # /tests/sample 内の .muasm ファイルをすべて取得
    test_files = glob.glob(os.path.join(test_dir, "**/*.muasm"), recursive=True)

    # .muasmファイルに対してテストを実行
    for test_file in test_files:
        metrics_proposed = process_single_file(test_file, "proposed")
        save_metrics(metrics_proposed, test_file, "proposed")
        metrics_baseline = process_single_file(test_file, "baseline")
        save_metrics(metrics_baseline, test_file, "baseline")

        # テスト結果を分析
        metrics_file_proposed = os.path.splitext(test_file)[0] + ".proposed.metrics"
        metrics_file_baseline = os.path.splitext(test_file)[0] + ".baseline.metrics"
        # compare_metrics(metrics_file_proposed, metrics_file_baseline)

        # 比較結果をDataFrameに追加
        comparison_result = compare_and_store_metrics(
            metrics_file_proposed, metrics_file_baseline, test_file
        )
        results_df = pd.concat([results_df, comparison_result], ignore_index=True)

    # 結果を一覧表示
    print("\nComparison Results (All Test Cases):")
    print(results_df)

    # 数値メトリクスの平均を計算して表示
    print("\nAverage Comparison Results (Numerical Metrics):")
    numerical_metrics = results_df.select_dtypes(include="number")
    print(numerical_metrics.mean())


if __name__ == "__main__":
    main()
