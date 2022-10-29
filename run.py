import argparse
import os
import traceback

from pandas import read_csv, read_excel
from stream_bit_rate.stream_bitrate_stats import BitrateStats


def parse_arguments():
    """
    Argument for the HTTP probe
    :return:
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="Calculate Stream Bit Rate",
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

def get_stream_metadata(arguments, row):
    """
    Get the stream metadata information.
    :return: Series, with metadata columns
    """
    try:
        print("Processing: ", str(row["Streams"]).strip())
        br = BitrateStats(
            row["Streams"],
            arguments.stream_type,
            arguments.aggregation,
            arguments.chunk_size,
            arguments.dry_run,
            arguments.verbose,
        )
        br.calculate_statistics()
        metadata = br.get_stream_metadata()

        row["Stream Type"] = metadata.get("stream_type")
        row["Average FPS"] = metadata.get("avg_fps")
        row["Average Bitrate"] = metadata.get("avg_bitrate")
        row["Probe Duration"] = metadata.get("chunk_size")
        row["Width"] = metadata.get("width")
        row["Height"] = metadata.get("height")
        row["Codec"] = metadata.get("codec_name")
        row["Codec Name"] = metadata.get("codec_long_name")
    except Exception as e:
        print("ERROR ", e)
        print(traceback.print_exc())

    return row


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

    # process the metadata for entire dataframe
    df_output = df.apply(lambda row: get_stream_metadata(arguments, row), axis=1, result_type='expand')
    print("OUTPUT file generated ", os.path.join(output_dir, f"{file_name}_output.{file_format}"))
    # output file generation
    if str(file_format).lower() in ["xlsx", "xls"]:
        df_output.to_excel(os.path.join(output_dir, f"{file_name}_output.{file_format}"), index=False)
    elif str(file_format).lower() in ["csv"]:
        df_output.to_csv(os.path.join(output_dir, f"{file_name}_output.{file_format}"), index=False)
    elif str(file_format).lower() in ["json"]:
        df_output.to_json(os.path.join(output_dir, f"{file_name}_output.{file_format}"), index=False)
    else:
        # default output format
        df_output.to_excel(os.path.join(output_dir, f"{file_name}_output.xlsx"), index=False)


