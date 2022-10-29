#!/usr/bin/env bash

# NOTE: this script should be run from the wallpapers root directory.

readme_body="""
A gallery of wallpapers for goats.

** Installation
*** on ArchLinux
one can use [[https://github.com/goatfiles/pkgbuilds/blob/main/x86_64/goat-wallpapers-git/PKGBUILD][the custom PKGBUILD for goats]] as follows:
#+begin_src bash
git clone https://github.com/goatfiles/pkgbuilds
cd ./pkgbuilds
./install.sh x86_64/goat-wallpapers-git
#+end_src
*** on another distribution of Linux
/Makefile and instructions *coming soon*/
** Usage
The wallpapers are installed by default in ~/usr/share/backgrounds/goat-wallpapers-git~.

Try having a look at them with ~feh /usr/share/backgrounds/goat-wallpapers-git/~ for instance!

** Ownership.
These wallpapers come from the internet. Diffusion and usage rights are not known for all of them.
*I do not own any of the wallpapers listed in this repo.*

If you stumble upon art or photos that you own or that you know and show that special rights have to be used to use or share them, *let me known and I will remove them immediately and without question!*"""

generate_file() {
    echo "* wallpapers"
    echo "$readme_body"

    printf "\n** Gallery\n"
    for fullname in $(ls wallpapers/*); do
        filename=$(basename "$fullname")
        printf "**** %s\n" "$filename"
        printf "#+CAPTION: %s\n" "$filename"
        printf "#+NAME: %s\n" "$fullname"
        printf "[[./%s]]\n\n" "$fullname"
    done
}

generate_file | tee README.org

# useful for inspecting readme after creation e.g. $ ./generate_preview.sh vim
[ -n "$1" ] && $1 README.org

exit 0
