#!/usr/bin/env python3
from typing import List, Tuple

import os
import argparse
from tqdm import tqdm
import tabulate

import numpy as np
import cv2


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


def main(*, path: str):
    filenames = sorted(os.listdir(path))

    wallpapers = load_images(filenames, path=path)

    shapes = [wallpaper.shape[:2] for wallpaper in wallpapers]

    valid_shapes = compute_all_valid_shapes(shapes)

    ratios = [w / h for h, w in shapes]
    are_good_ratios = [is_good_ratio(w, h) for h, w in shapes]
    closest_shapes = [
        get_closest_shape(w, h, valid_shapes=valid_shapes) for h, w in shapes
    ]
    closest_ratios = [w / h for h, w in closest_shapes]
    are_closest_good_ratios = [is_good_ratio(w, h) for h, w in closest_shapes]

    table = tabulate.tabulate(
        zip(
            filenames,
            shapes,
            ratios,
            are_good_ratios,
            closest_shapes,
            closest_ratios,
            are_closest_good_ratios,
        ),
        headers=[
            "filenames",
            "shapes",
            "ratios",
            "are_good_ratios",
            "closest_shapes",
            "closest_ratios",
            "are_closest_good_ratios",
        ],
    )
    print(table)

    for wallpaper, closest_shape, filename in tqdm(
        list(zip(wallpapers, closest_shapes, filenames)), desc="Resizing the images"
    ):
        height, width = wallpaper.shape[:2]
        if not is_good_ratio(width, height):
            resized_wallpaper = cv2.resize(wallpaper, closest_shape[::-1])
            cv2.imwrite(os.path.join(path, filename), resized_wallpaper)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        required=True,
        type=str,
        help="The path to the wallpapers.",
    )

    args = parser.parse_args()

    main(path=args.path)
