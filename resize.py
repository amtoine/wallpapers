#!/usr/bin/env python3
from typing import List, Tuple

import os
import argparse
from tqdm import tqdm

import numpy as np
import cv2
from colorama import Fore, Back, Style


def load_image(filename: str, *, path: str) -> np.ndarray:
    return cv2.imread(os.path.join(path, filename))


def load_images(filenames: List[str], *, path: str) -> List[np.ndarray]:
    images = []
    for filename in tqdm(filenames, desc=f"Loading images in {path}"):
        image = load_image(filename, path=path)
        images.append(image)
    return images


def is_good_ratio(
    width: int,
    height: int,
    *,
    ratio: Tuple[int, int] = (16, 9),
) -> bool:
    return bool(width == int(height * ratio[0] / ratio[1]))


def get_closest_shape(
    width: int,
    height: int,
    *,
    valid_shapes: np.ndarray,
    ratio: Tuple[int, int] = (16, 9),
) -> Tuple[int, int]:
    if is_good_ratio(width, height, ratio=ratio):
        return (height, width)

    bad_shape = np.array([height, width])
    index = np.sum(np.square(valid_shapes - bad_shape), axis=1).argmin()
    return valid_shapes[index]


def compute_all_valid_shapes(
    shapes: np.ndarray,
    *,
    ratio: Tuple[int, int] = (16, 9),
) -> np.ndarray:
    ratio = np.array(ratio)
    max_ratio = np.max(shapes / ratio).astype(int)
    ratio_range = np.arange(1, max_ratio + 1)
    valid_shapes = np.dot(ratio_range[:, None], ratio[None, :])
    return valid_shapes[:, ::-1]


def show_image(image: np.ndarray, *, title: str = "Title") -> None:
    cv2.imshow(title, image)
    cv2.waitKey(0)


def main(*, path: str, ratio: Tuple[int, int], margin: float, verbose: bool) -> None:
    filenames = sorted(os.listdir(path))
    wallpapers = load_images(filenames, path=path)

    shapes = [wallpaper.shape[:2] for wallpaper in wallpapers]
    valid_shapes = compute_all_valid_shapes(shapes, ratio=ratio)

    for wallpaper, filename in zip(wallpapers, filenames):
        height, width = wallpaper.shape[:2]
        if is_good_ratio(width, height, ratio=ratio):
            if verbose:
                print(f"{Fore.GREEN}[OK...]{Style.RESET_ALL} {filename}: Skipping...")
        elif abs(width / height - ratio[0] / ratio[1]) <= margin:
            print(
                f"{Fore.YELLOW}[WARN.]{Style.RESET_ALL} {filename}: Resizing...", end=""
            )
            print("done!")
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {filename}: Manual...")


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
        "-r",
        "--ratio",
        nargs=2,
        type=int,
        default=[16, 9],
        help="TODO.",
    )
    parser.add_argument(
        "-m",
        "--margin",
        type=float,
        default=0.17778,
        help="TODO.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="TODO.",
    )

    args = parser.parse_args()

    main(path=args.path, ratio=args.ratio, margin=args.margin, verbose=args.verbose)
