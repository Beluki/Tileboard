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
        -gravity south            \
        -splice 0x5               \
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
rm Screenshot2-a.png Screenshot2-b.png Screenshot2-c.png


# Screenshot3:
# Dots and crosses:

# knight moves:
tileboard 8/8/8/8/3n4/8/8/8 Screenshot3-a.png                            \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30                           \
    --dots B5 B3 C6 C2 E6 E2 F5 F3

add_image_label_southwest Screenshot3-a.png "
    --dots B5 B3 C6 C2 E6 E2 F5 F3
"

# pawn moves:
tileboard 8/8/8/8/8/8/3P4/8 Screenshot3-b.png                            \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30                           \
    --dots D3 D4                                                         \
    --crosses C3 E3

add_image_label_southwest Screenshot3-b.png "
    --dots D3 D4
    --crosses C3 E3
"

# king moves with check:
tileboard 7K/5k2/8/8/6q1/8/8/8 Screenshot3-c.png                         \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30                           \
    --dots H7                                                            \
    --dots-color green                                                   \
    --crosses G7 G8                                                      \
    --crosses-color darkred

add_image_label_southwest Screenshot3-c.png "
    --dots H7
    --dots-color green
    --crosses G7 G8
    --crosses-color darkred
"

combine_images_horizontally Screenshot3-a.png Screenshot3-b.png Screenshot3-c.png Screenshot3.png
rm Screenshot3-a.png Screenshot3-b.png Screenshot3-c.png


# Screenshot4:
# Small chess variants:

# Gardner:
tileboard rnbqk/ppppp/5/PPPPP/RNBQK Screenshot4-a.png                    \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot4-a.png "Gardner 5x5"

# MinitChess:
tileboard kqbnr/ppppp/5/5/PPPPP/RNBQK Screenshot4-b.png                  \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot4-b.png "MinitChess 5x6"

# Los Alamos:
tileboard rnqknr/pppppp/6/6/PPPPPP/RNQKNR Screenshot4-c.png              \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot4-c.png "Los Alamos 6x6"

# Duchess:
tileboard rnqnr/ppppp/5/5/5/PPPPP/RNQNR Screenshot4-d.png                \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot4-d.png "Duchess"

combine_images_horizontally Screenshot4-a.png Screenshot4-b.png Screenshot4-c.png Screenshot4-d.png Screenshot4.png
rm Screenshot4-a.png Screenshot4-b.png Screenshot4-c.png Screenshot4-d.png


# Screenshot5:
# Big board:
tileboard rnbqkbnrRNQKNRrnqknrRNBQKBNR/ppppppppPPPPPPppppppPPPPPPPP/9991/9991/9991/9991/9991/9991/PPPPPPPPppppppPPPPPPpppppppp/RNBQKBNRrnqknrRNQKNRrnbqkbnr Screenshot5.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot5.png "28x10"

# Screenshot6:
# Irregular boards, Cam:
tileboard 0001/003/05/2n1n2/1ppppp1/7/7/7/1PPPPP1/2N1N2/05/003/0001 Screenshot6.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                         \
    --tileset-folder ../Source/Tiles/merida/30                                      \
    --dots D1 D13

add_image_label_center Screenshot6.png "Cam"

cp *.png ../Screenshot
