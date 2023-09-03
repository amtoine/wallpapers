#!/usr/bin/env nu

const README = "README.org"
const README_HEADER = "* wallpapers

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

If you stumble upon art or photos that you own or that you know and show that special rights have to be used to use or share them, *let me known and I will remove them immediately and without question!*

** Gallery"

def preview [filename: path, name: string, --level: int = 4]: nothing -> string {
    [
        $"('*' * $level) ($name)"
        $"#+CAPTION: ($name)"
        $"#+NAME: ($filename)"
        $"[[./($filename)]]\n\n"
    ]
    | str join "\n"
}

def main [] {
    $README_HEADER ++ "\n" | save --force $README

    ls wallpapers/ | sort-by type | each {|it|
        match $it.type {
            "dir" => {
                preview $it.name $it.name --level 3 | save --force --append $README

                let readme = $it.name | path join $README
                "" | save --force $readme

                ls ($it.name | path join "**/*") | where type == file | each {|file|
                    print -n $"(ansi erase_line)($file.name)\r"

                    preview ($file.name | path basename) ($file.name | path basename) --level 2
                        | save --force --append $readme
                }
            },
            "file" => {
                preview $it.name ($it.name | path basename) --level 3
                    | save --force --append $README
            },
        }
    }

    null
}
