import argparse
import os
import sys
import traceback


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
    parser.add_argument("no_of_stream", help="No of streams to play via ffplay", type=int)

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Do not run command, just show what would be done",
    )

    return parser.parse_args()


def print_stderr(msg):
    print(msg, file=sys.stderr)


def run_command(cmd, dry_run):
    if dry_run:
        print_stderr("[cmd] " + " ".join(cmd))
        return

    os.system(" ".join(cmd))


def play_stream(stream_count, dry_run):
    try:

        for i in range(1, stream_count + 1):
            cmd = [
                "ffplay",
                f"http://10.10.11.52:550{i}/stream{i}",
                "&"
            ]
            cmd = [param for param in cmd if param]

            run_command(cmd, dry_run)
        if dry_run:
            print_stderr("Aborting prematurely, dry-run specified")
            sys.exit(0)

    except Exception:
        print("Error in calculating statistics")
        print(traceback.print_exc())


if __name__ == '__main__':
    arguments = parse_arguments()
    print('No Of streams for play : '.format(arguments.no_of_stream))
    play_stream(int(arguments.no_of_stream), arguments.dry_run)
