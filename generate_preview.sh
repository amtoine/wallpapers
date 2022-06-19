#!/usr/bin/env bash

# NOTE: this script should be run from the wallpapers root directory.

nb_note="""
A gallery of wallpapers I use for my laptop config.

| ![montage.png](montage.png) |
|:--:|
| ***Overview of the wallpapers inside the repo.** Images have been stretched to fit inside squares.* |

## Ownership.
These wallpapers come from the internet. Diffusion and usage rights are not known for all of them.
**I do not own any of the wallpapers listed in this repo.**
If you stumble upon art or photos that you own or that you know and show that special rights have to be used to use or share them, **let me known and I will remove them immediately and without question!**"""

generate_file() {
    echo "<!-- markdownlint-disable MD026 -->"
    echo "# wallpapers"
    echo "$nb_note"

    for fullname in $(ls wallpapers/*); do
        filename=$(basename "$fullname")
        printf "\n## %s\n\n![%s](%s)\n" "$filename" "$fullname" "$fullname"
    done
}

rm README.md; generate_file >>README.md

# useful for inspecting readme after creation e.g. $ ./generate_preview.sh vim
[ -n "$1" ] && $1 README.md

exit 0
