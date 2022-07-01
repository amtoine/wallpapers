#!/usr/bin/env bash

for wallpaper in ./wallpapers/*;
do
    name=$(basename "$wallpaper")
    size=$(identify "$wallpaper" | cut -d' ' -f3);
    new_location="./wallpapers/$size"
    # echo "$name ($wallpaper): $size -> $new_location"
    mkdir -p "$new_location"
    mv "$wallpaper" "$new_location/$name"
done
