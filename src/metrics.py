import logging
import os


def save_metrics(metrics, test_file, algorithm):
    """
    メトリクスをファイルに保存する関数。

    Args:
        metrics: 保存するメトリクスの辞書
        test_file: テストファイルのパス
        algorithm: 実行したアルゴリズム
    """
    metrics_filename = os.path.splitext(test_file)[0] + f".{algorithm}.metrics"
    with open(metrics_filename, "w") as f:
        f.write("metric,value\n")
        for key, value in metrics.items():
            f.write(f"{key},{value}\n")
    logging.info(f"  Metrics saved to: {metrics_filename}")
