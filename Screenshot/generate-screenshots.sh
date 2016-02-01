#!/bin/bash

#

tileboard() {
    ../Tileboard.py $@
}

add_image_label_southwest() {
    /c/ImageMagick/convert   "$1" \
        -background none          \
        -gravity southwest        \
        -font Consolas label:"$2" \
        -append "$1"
}


add_image_label_center() {
    /c/ImageMagick/convert   "$1" \
        -background none          \
        -gravity center           \
        -font Consolas label:"$2" \
        -append "$1"
}

combine_images_horizontally() {
    /c/ImageMagick/montage        \
        -background none          \
        -tile x1                  \
        -gravity north            \
        -geometry +1 $@
}


tileboard rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR chess1.png
#tileboard rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR chess2.png --tileset-folder Tiles/merida/30
#tileboard rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR chess3.png --tileset-folder Tiles/merida/30

add_image_label_southwest chess1.png "
--checkerboard-color1 #FDFFD5
--checkerboard-color2 #B3B174
--border-color #313100
--border-font-color #FDFF98
"

#combine_images_horizontally chess1.png chess2.png chess3.png result.png
#rm chess1.png chess2.png chess3.png

