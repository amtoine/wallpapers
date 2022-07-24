#!/usr/bin/env python3

import os
import cv2
from tqdm import tqdm
import numpy as np
from colorama import Fore, Style
from typing import List
import argparse


# log functions.
def _colored_print(*msg, color, log_msg: str):
    print(f"{color}[{log_msg}]{Style.RESET_ALL}", *msg)


def error(*msg):
    _colored_print(*msg, color=Fore.RED, log_msg="ERROR..")


def warning(*msg):
    _colored_print(*msg, color=Fore.YELLOW, log_msg="WARNING")


def info(*msg):
    _colored_print(*msg, color=Fore.BLUE, log_msg="INFO...")


# main functions.
def load_image(filename: str, *, path: str) -> np.ndarray:
    fullname = os.path.join(path, filename)
    return cv2.imread(fullname)


def load_images(filenames: List[str], *, path: str) -> List[np.ndarray]:
    filenames_bar = tqdm(filenames, desc=f"Loading images from '{path}'")
    images = [load_image(filename, path=path) for filename in filenames_bar]
    return images


def main(*, path: str, desired_shape: np.ndarray, verbose: bool) -> None:
    filenames = os.listdir(path)
    filenames = sorted(filenames)

    images = load_images(filenames, path=path)

    for image, filename in zip(images, filenames):
        if image is not None:
            shape = np.array(image.shape[:2])
            if np.any(shape < desired_shape):
                warning(f"{filename} is too small: {shape}")
            elif verbose:
                info(f"{filename} is large enough: {shape}")
        else:
            error(f"{filename} is not a valid image...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        required=True,
        type=str,
        help="The path to the wallpapers.",
    )
    parser.add_argument(
        "-s",
        "--shape",
        nargs=2,
        type=int,
        default=[1080, 1920],
        help="TODO.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="TODO.",
    )

    args = parser.parse_args()

    main(
        path=args.path,
        desired_shape=np.array(args.shape),
        verbose=args.verbose
    )
