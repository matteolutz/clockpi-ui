import argparse


def get_arg_parser():
    parser = argparse.ArgumentParser(
        prog="clockpi-ui",
    )

    parser.add_argument("-s", "--serial", type=str, help="Serial port for LED control")
    parser.add_argument(
        "-f", "--fullscreen", action="store_true", help="Run in fullscreen mode"
    )

    return parser
