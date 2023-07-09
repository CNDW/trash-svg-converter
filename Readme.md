TrashMessengerBags product mock requirements

SVG file specifications -

The files must be in Adobe Illustrator or SVG format. Use a minimal amount of points and lines to keep the file clean and lightweight

The target canvas size is 792 wide by 650 tall - the size does not need to be exact, the converter will scale the image down to 762 wide with the same aspect ratio so the height can be adjusted as needed.

The final output must have the dynamic portions of the mockup tagged with the following colors

primary - #ff0200 red
secondary - #0a24f7 blue
liner - #00c600 lime green
webbing - #ff00ff purple
stitching - #fff200 yellow
trim - #009e78 dark green
buckle - #00ffff turquoise
velcro - #ffa600 orange

try to avoid using any colors aside from black(#000000), white(#ffffff), or gray(#a3a3a3). Exceptions can be made but they need to be manually applied to the converter script. The script will be able to match similar colors, but please try to use those exact colors to avoid complications or mis-targetting the sections

Conversion Process -

1) Download the converter script and using `Python` install the `requirements.txt`