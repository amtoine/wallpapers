#!/usr/bin/env nu

def main [
    directory: path
    --destinations: list<path> = [other trash real waifu abstract fun-tech]
] {
    $destinations | each {|destination|
        mkdir $destination
    }

    ls $directory | each {|file|
        devour feh --fullscreen $file.name
        let destination = ($destinations | input list --fuzzy
            $"Please choose a destination for ($file.name)"
        )
        mv --force $file.name $destination
    }
}
