import logging
import os
import pandas as pd


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


def analyze_spectector_result(spectector_result, metrics):
    """
    spectectorの実行結果を解析し、metricsを更新する。

    Args:
        spectector_result: SpectectorResultオブジェクト
        metrics: メトリクスを格納する辞書
    """
    if spectector_result.stdout:
        lines = spectector_result.stdout.strip().split("\n")
        if lines and lines[-1] == "[program is safe]":
            metrics["leak"] = False
            metrics["successful"] = True
        else:
            metrics["leak"] = True
            metrics["successful"] = True


def compare_metrics(metrics_file1, metrics_file2):
    """
    2つのメトリクスファイルを比較し、比較結果を出力する関数。

    Args:
        metrics_file1: 1つ目のメトリクスファイルのパス
        metrics_file2: 2つ目のメトリクスファイルのパス
    """
    try:
        df1 = pd.read_csv(metrics_file1)
        df2 = pd.read_csv(metrics_file2)

        # 'metric' 列をインデックスに設定
        df1.set_index("metric", inplace=True)
        df2.set_index("metric", inplace=True)

        print(f"Comparing {metrics_file1} and {metrics_file2}:")

        # 各メトリクスを比較
        for metric in df1.index:
            if metric in df2.index:
                value1 = df1.loc[metric, "value"]
                value2 = df2.loc[metric, "value"]

                # 数値に変換できるか試みる
                try:
                    num_value1 = float(value1)
                    num_value2 = float(value2)

                    # 数値の比較
                    if num_value1 > num_value2:
                        diff = num_value1 - num_value2
                        print(
                            f"  {metric}: {num_value1} > {num_value2} (diff: {diff:.6f})"
                        )
                    elif num_value1 < num_value2:
                        diff = num_value2 - num_value1
                        print(
                            f"  {metric}: {num_value1} < {num_value2} (diff: {diff:.6f})"
                        )

                except ValueError:
                    # 文字列の比較
                    if value1 != value2:
                        print(f"  {metric}: {value1} != {value2}")
            else:
                print(f"  {metric}: Not found in {metrics_file2}")

    except FileNotFoundError:
        print("Error: One or both of the metrics files were not found.")
    except Exception as e:
        print(f"Error during comparison: {e}")

def compare_and_store_metrics(metrics_file1, metrics_file2, test_file):
    """
    2つのメトリクスファイルを比較し、比較結果をDataFrameとして返す関数。

    Args:
        metrics_file1: 1つ目のメトリクスファイルのパス
        metrics_file2: 2つ目のメトリクスファイルのパス
        test_file: テストファイルのパス

    Returns:
        DataFrame: 比較結果を格納したDataFrame
    """
    try:
        df1 = pd.read_csv(metrics_file1)
        df2 = pd.read_csv(metrics_file2)

        # 'metric' 列をインデックスに設定
        df1.set_index("metric", inplace=True)
        df2.set_index("metric", inplace=True)

        # 比較結果を格納する辞書
        comparison_dict = {"test_file": test_file}

        # 各メトリクスを比較
        for metric in df1.index:
            if metric in df2.index:
                value1 = df1.loc[metric, "value"]
                value2 = df2.loc[metric, "value"]

                # 数値に変換できるか試みる
                try:
                    num_value1 = float(value1)
                    num_value2 = float(value2)

                    # 数値の比較
                    comparison_dict[metric] = num_value1 - num_value2

                except ValueError:
                    # 文字列の比較
                    comparison_dict[metric] = value1 if value1 != value2 else "same"

            else:
                comparison_dict[metric] = "Not found in baseline"

        return pd.DataFrame([comparison_dict])

    except FileNotFoundError:
        print("Error: One or both of the metrics files were not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error during comparison: {e}")
        return pd.DataFrame()