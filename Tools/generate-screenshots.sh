#!/bin/bash

tileboard() {
    ../Source/Tileboard.py $@
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


# Screenshot1:
# Regular chess:

tileboard rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR Screenshot1.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf           \
    --tileset-folder ../Source/Tiles/merida/42


# Screenshot2:
# Colors:

# excelsior:
tileboard n1rb4/1p3p1p/1p6/1R5K/8/p3p1PN/1PP1R3/N6k Screenshot2-a.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf           \
    --tileset-folder ../Source/Tiles/merida/30                        \
    --checkerboard-color1 '#FDFFD5'                                   \
    --checkerboard-color2 '#B3B174'                                   \
    --border-color '#313100'                                          \
    --border-font-color '#FDFF98'

add_image_label_southwest Screenshot2-a.png "
    --checkerboard-color1 '#FDFFD5'
    --checkerboard-color2 '#B3B174'
    --border-color '#313100'
    --border-font-color '#FDFF98'
"

# grotesque moreover:
tileboard 8/8/8/1k3p2/p1p1pPp1/PpPpP1Pp/1P1P3P/QNK2NRR Screenshot2-b.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30                           \
    --checkerboard-color1 '#EBF3FF'                                      \
    --checkerboard-color2 '#286EA0'                                      \
    --border-color '#EBF3FF'                                             \
    --border-font-color '#1A486C'

add_image_label_southwest Screenshot2-b.png "
    --checkerboard-color1 '#EBF3FF'
    --checkerboard-color2 '#286EA0'
    --border-color '#EBF3FF'
    --border-font-color '#1A486C'
"

# lacny:
tileboard 8/3pK3/b2p4/3Q3B/qRp2Nn1/r3kNB1/rRp5/n5b1 Screenshot2-c.png    \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30                           \
    --checkerboard-color1 '#FFC7BD'                                      \
    --checkerboard-color2 '#F28E98'                                      \
    --border-color '#E7E4D3'                                             \
    --border-font-color '#8D7966'

add_image_label_southwest Screenshot2-c.png "
    --checkerboard-color1 '#FFC7BD'
    --checkerboard-color2 '#F28E98'
    --border-color '#E7E4D3'
    --border-font-color '#8D7966'
"

combine_images_horizontally Screenshot2-a.png Screenshot2-b.png Screenshot2-c.png Screenshot2.png


