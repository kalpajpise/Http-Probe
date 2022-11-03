import argparse
import os
import sys
import traceback


def parse_arguments():
    """
    Argument for the Stream Video http
    :return:
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="Generate Multiple Http Stream",
        description="Code generates multiple streams through FFmpeg via http protocols.",
    )
    parser.add_argument(
        "input_no_of_streams",
        help="Input No Of streams required to stream in background",
        type=int,
    )

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Do not run command, just show what would be done",
    )

    parser.add_argument(
        "-i", "--input", default="main_1.mp4", help="Input File for streams"
    )

    parser.add_argument(
        "-k", "--kill-all", help="Signal to kill all streams of ffmpeg"
    )

    return parser.parse_args()


def print_stderr(msg):
    print(msg, file=sys.stderr)


def run_command(cmd, dry_run):
    """
    Run a command directly
    """

    if dry_run:
        print_stderr("[cmd] " + " ".join(cmd))
        return

    os.system(" ".join(cmd))

    # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()

    # if process.returncode == 0:
    #     return stdout.decode("utf-8"), stderr.decode("utf-8")
    # else:
    #     print_stderr("[error] running command: {}".format(" ".join(cmd)))
    #     print_stderr(stderr.decode("utf-8"))
    # return None, None


def generate_stream_cmd(no_of_stream, dry_run, file):
    """
    Genrating FFmpeg stream command for multiple streams
    """

    try:
        for i in range(1, no_of_stream + 1):
            cmd = [
                "ffmpeg",
                "-re",
                "-stream_loop",
                "-1",
                "-i",
                file,
                "-c",
                "copy",
                "-listen",
                "1",
                "-movflags",
                "frag_keyframe+empty_moov",
                "-f",
                "mp4",
                f"http://0.0.0.0:550{i}/stream{i}",
                "&",
            ]

            cmd = [param for param in cmd if param]

            run_command(cmd, dry_run)

            if dry_run:
                print_stderr("Aborting prematurely, dry-run specified")
                sys.exit(0)

    except Exception:
        print("Error in calculating statistics")
        print(traceback.print_exc())


if __name__ == "__main__":
    arguments = parse_arguments()
    print("Total number of streams executing: ", arguments.input_no_of_streams)
    print("The command is runing on dry run") if arguments.dry_run else None
    generate_stream_cmd(int(arguments.input_no_of_streams), arguments.dry_run, str(arguments.input))
