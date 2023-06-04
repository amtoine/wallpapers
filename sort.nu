#!/usr/bin/env nu

let destinations = [other trash real waifu abstract fun-tech]

$destinations | each {|destination|
    mkdir $destination
}

ls wallpapers/ | each {|file|
    devour feh --fullscreen $file.name
    let destination = ($destinations | input list --fuzzy
        $"Please choose a destination for ($file.name)"
    )
    mv --force $file.name $destination
}
