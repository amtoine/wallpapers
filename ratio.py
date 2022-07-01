#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
import tqdm

DIRECTORY = os.path.expanduser("~/ghq/github.com/a2n-s/wallpapers/wallpapers")
size_map = {os.path.join(DIRECTORY, sub_dir): list(map(int, sub_dir.split("x"))) for sub_dir in tqdm.tqdm(os.listdir(DIRECTORY), desc="extract")}
sizes = np.array(list(size_map.values()))

plt.style.use("dark_background")


def get_key(x: int, y: int) -> str:
    return f"{x:4>}, {y:4>}"


def compute_resize_map(data):
    verticals = []
    resize_map = {}

    for name, size in tqdm.tqdm(data.items(), desc="resize map"):
        x, y = size
        if y >= x:
            verticals.append(name)

        comp = int(y * 16 / 9 - x)
        if comp != 0:
            if comp < 0:
                v = y // 9 * 9
                u = v * 16 / 9
            else:
                u = x // 16 * 16
                v = u * 9 / 16

            assert not u % 1
            assert not v % 1
            u = int(u)
            v = int(v)
            assert v == 9 / 16 * u

            resize_map[get_key(x, y)] = [u, v]

    return resize_map, verticals


def plot_wallpaper_data(data, resize_map, *, threshold: int = 50, scale: int = 50):
    for name, size in tqdm.tqdm(data.items(), desc="plot"):
        nb_wallpapers = len(os.listdir(name))
        marker_size = np.log(nb_wallpapers + 1)*scale

        x, y = size
        comp = int(y * 16 / 9 - x)
        if y >= x:
            plt.scatter(x, y, s=200, marker="+", color="red")
        else:
            color = "green" if comp == 0 else None
            if nb_wallpapers > threshold:
                plt.scatter(x, y, s=marker_size, label=name.split("/")[-1], c=color)
            else:
                plt.scatter(x, y, s=marker_size, c=color)

        if comp != 0:
            u, v = resize_map[get_key(x, y)]
            plt.plot([u, x], [v, y], linestyle="--")


def plot_ratio(ratio_x: int, ratio_y: int, line: str = None, c: str = None) -> None:
    t = np.linspace(0, int(min(sizes.max(axis=0) / np.array((ratio_x, ratio_y)))), 10)
    plt.plot(t * ratio_x, t * ratio_y, label=f"{ratio_x}:{ratio_y}", linestyle=line, color=c)


resize_map, verticals = compute_resize_map(size_map)
for original, (u, v) in resize_map.items():
    print(f"{original} -> {u:>4}, {v:>4}")
print(verticals)

plot_ratio(16, 9)
plot_ratio(1, 1, line="--", c="red")
plot_wallpaper_data(size_map, resize_map, threshold=10)

plt.title("Wallpapers sizes distribution")
plt.xlabel("horizontal pixels")
plt.ylabel("vertical pixels")

plt.legend()
plt.show()
