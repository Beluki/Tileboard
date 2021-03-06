#!/bin/bash

# This is the script that generates all the Screenshots in the Tileboard README.
# It's meant to be run from MSYS2.

# Depends on:  Tileboard (relative path)
# and ImageMagick (hardcoded to /c/ImageMagick).
# There's zero error handling.


# Draw a board with the given parameters:

tileboard() {
    ../Source/Tileboard.py $@
}

# Put a label at the bottom left corner of an image:

add_image_label_southwest() {
    /c/ImageMagick/convert   "$1" \
        -background none          \
        -gravity southwest        \
        -font Consolas label:"$2" \
        -append "$1"
}

# Put a label at the bottom center of an image:

add_image_label_center() {
    /c/ImageMagick/convert   "$1" \
        -background none          \
        -gravity south            \
        -splice 0x5               \
        -font Consolas label:"$2" \
        -append "$1"
}

# Put images side by side horizontally:

combine_images_horizontally() {
    /c/ImageMagick/montage        \
        -background none          \
        -tile x1                  \
        -gravity north            \
        -geometry +2 $@
}

# Put images side by side vertically:

combine_images_vertically() {
    /c/ImageMagick/montage        \
        -background none          \
        -tile 1x                  \
        -gravity north            \
        -geometry +4 $@
}


# Screenshot1:
# Regular chess:

tileboard rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR Screenshot1.png    \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/42


# Screenshot2:
# Colors:

# excelsior:
tileboard n1rb4/1p3p1p/1p6/1R5K/8/p3p1PN/1PP1R3/N6k Screenshot2-a.png    \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30                           \
    --checkerboard-color1 '#FDFFD5'                                      \
    --checkerboard-color2 '#B3B174'                                      \
    --border-color '#313100'                                             \
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

combine_images_horizontally Screenshot2-{a,b,c}.png Screenshot2.png
rm Screenshot2-{a,b,c}.png


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

combine_images_horizontally Screenshot3-{a,b,c}.png Screenshot3.png
rm Screenshot3-{a,b,c}.png


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

add_image_label_center Screenshot4-d.png "Duchess 5x7"

combine_images_horizontally Screenshot4-{a,b,c,d}.png Screenshot4.png
rm Screenshot4-{a,b,c,d}.png


# Screenshot5:
# Big board:
tileboard rnbqkbnrRNQKNRrnqknrRNBQKBNR/ppppppppPPPPPPppppppPPPPPPPP/9991/9991/9991/9991/9991/9991/PPPPPPPPppppppPPPPPPpppppppp/RNBQKBNRrnqknrRNQKNRrnbqkbnr Screenshot5.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot5.png "28x10"


# Screenshot6:
# Irregular boards:

# Cam:
tileboard 0001/003/05/2n1n2/1ppppp1/7/7/7/1PPPPP1/2N1N2/05/003/0001 Screenshot6-a.png   \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                             \
    --tileset-folder ../Source/Tiles/merida/30                                          \
    --dots D1 D13

add_image_label_center Screenshot6-a.png "Cam"

# Amazons:
tileboard 303Q2/1q1005/30Q5/100002q2/0070/4q5/201Q5/4q5/2001103/401Q3 Screenshot6-b.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                             \
    --tileset-folder ../Source/Tiles/merida/30

add_image_label_center Screenshot6-b.png "Amazons (the board changes while playing)"

combine_images_horizontally Screenshot6-{a,b}.png Screenshot6.png
rm Screenshot6-{a,b}.png


# Screenshot7:
# Sizes:

tileboard 111/1r1/111 Screenshot7-a.png                                  \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/28

add_image_label_center Screenshot7-a.png "28px"

tileboard 111/1b1/111 Screenshot7-b.png                                  \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/36

add_image_label_center Screenshot7-b.png "36px"

tileboard 111/1n1/111 Screenshot7-c.png                                  \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/52

add_image_label_center Screenshot7-c.png "52px"

tileboard 111/1k1/111 Screenshot7-d.png                                  \
    --border-font ../Source/Font/LiberationMono-Regular.ttf              \
    --tileset-folder ../Source/Tiles/merida/88

add_image_label_center Screenshot7-d.png "88px"

combine_images_horizontally Screenshot7-{a,b,c,d}.png Screenshot7.png
rm Screenshot7-{a,b,c,d}.png


# Screenshot8:
# Tilesets:

# alpha:
tileboard rnbqkpRNBQKP Screenshot8-a.png                                       \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                    \
    --tileset-folder ../Source/Tiles/alpha/52                                  \
    --border-disable

add_image_label_center Screenshot8-a.png "--tileset-folder Tiles/alpha/52"

# merida:
tileboard rnbqkpRNBQKP Screenshot8-b.png                                       \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                    \
    --tileset-folder ../Source/Tiles/merida/52                                 \
    --border-disable

add_image_label_center Screenshot8-b.png "--tileset-folder Tiles/merida/52"

# usf:
tileboard rnbqkpRNBQKP Screenshot8-c.png                                       \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                    \
    --tileset-folder ../Source/Tiles/usf/52                                    \
    --border-disable

add_image_label_center Screenshot8-c.png "--tileset-folder Tiles/usf/52"

combine_images_vertically Screenshot8-{a,b,c}.png Screenshot8.png
rm Screenshot8-{a,b,c}.png


# Screenshot9:
# Beyond chess:

# checkers:
tileboard 1w1w1w1w/w1w1w1w1/1w1w1w1w/8/8/b1b1b1b1/1b1b1b1b/b1b1b1b1 Screenshot9-a.png \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                           \
    --tileset-folder checkers/40

add_image_label_center Screenshot9-a.png "Checkers"

# lines of action:
tileboard 1bbbbbb1/w6w/w6w/w6w/w6w/w6w/w6w/1bbbbbb1 Screenshot9-b.png                 \
    --border-font ../Source/Font/LiberationMono-Regular.ttf                           \
    --tileset-folder checkers/40

add_image_label_center Screenshot9-b.png "Lines of action"

combine_images_horizontally Screenshot9-{a,b}.png Screenshot9.png
rm Screenshot9-{a,b}.png


# Screenshot10:
# Other games:

# freegemas:
tileboard ygrpgowb/bopgwrrb/bbgrrwgw/wgrbpyww/wwopypgy/gwpbwrbo/gyopygrb/rgwwygpg Screenshot10.png \
    --outer-outline-color '#735A4C'                                                                \
    --checkerboard-color1 '#A5806B'                                                                \
    --checkerboard-color2 '#8E6E61'                                                                \
    --tileset-folder freegemas/65                                                                  \
    --border-disable


# Done:
# Move to the Screenshots folder:

cp *.png ../Screenshot
rm *.png

