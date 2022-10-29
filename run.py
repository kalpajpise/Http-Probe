import argparse
import os
import traceback

from pandas import read_csv, read_excel


def parse_arguments():
    """
    Argument for the HTTP probe
    :return:
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Stream Metadata Parser",
    )
    parser.add_argument("input_file", help="Input File for list of streams")

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Do not run command, just show what would be done",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose output"
    )

    parser.add_argument(
        "-s",
        "--stream-type",
        default="video",
        choices=["video", "audio"],
        help="Stream type to analyze",
    )

    parser.add_argument(
        "-a",
        "--aggregation",
        default="time",
        choices=["time", "gop"],
        help="Window for aggregating statistics, either time-based (per-second) or per GOP",
    )

    parser.add_argument(
        "-c",
        "--chunk-size",
        type=float,
        default=2.0,
        help="Custom aggregation window size in seconds. Probe time in gop",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default='output',
        help="output directory",
    )

    parser.add_argument(
        "-output_format",
        "--output-format",
        type=str,
        default="excel",
        choices=["csv", "excel", "tsv", "json"],
        help="output in which format",
    )

    return parser.parse_args()



def run():
    """
    Run the Stream bitrate stats module for list of streams
    """
    arguments = parse_arguments()
    stream_list_file = str(arguments.input_file).lower()
    output_dir = arguments.output_dir


    # check whether the input exists
    if not os.path.exists(stream_list_file):
        raise FileNotFoundError(f"List of stream file: {stream_list_file} not found")

    # check which type of input.
    if ".csv" in stream_list_file:
        df = read_csv(stream_list_file)
    elif (".xlsx" in stream_list_file) or (".xlx" in stream_list_file):
        df = read_excel(stream_list_file, engine='openpyxl')
    else:
        raise Exception("Stream template file format is not supported %s", stream_list_file)
    
    if "Streams" not in df:
        raise Exception("Please ensure the file has 'Streams' column name")
    print("Probe Duration: ", arguments.chunk_size)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # get filename from argument
    path, file_path = os.path.split(stream_list_file)

    file_name = file_path.split(".")[0]
    file_format = file_path.split(".")[-1]

    df["Streams"] = df["Streams"].str.strip()