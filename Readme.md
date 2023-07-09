# TrashMessengerBags product mock requirements

## SVG file specifications 

The files must be in Adobe Illustrator or SVG format. Use a minimal amount of points and lines to keep the file clean and lightweight

The target canvas size is 792 wide by 650 tall - the size does not need to be exact, the converter will scale the image down to 762 wide with the same aspect ratio so the height can be adjusted as needed.

The final output must have the dynamic portions of the mockup tagged with the following colors

- primary - #ff0200 red
- secondary - #0a24f7 blue
- liner - #00c600 lime green
- webbing - #ff00ff purple
- stitching - #fff200 yellow
- trim - #009e78 dark green
- buckle - #00ffff turquoise
- velcro - #ffa600 orange

try to avoid using any colors aside from black(#000000), white(#ffffff), or gray(#a3a3a3). Exceptions can be made but they need to be manually applied to the converter script. The script will be able to match similar colors, but please try to use those exact colors to avoid complications or mis-targetting the sections

## Conversion Process

The converter script is a little rough around the edges and may need some manual tweaking to get the exact results you need based on the input files, but _should work out of the box_

1) Download the converter script into it's own folder 
1) using `Python 3.11+` install the `requirements.txt`
1) if the raw files are in `.ai` format, convert them using Illustrator or [use the online ai to svg converter here](https://cloudconvert.com/)
1) place the `.svg` files in a `svgs` folder in the same directory that the converter script was downloaded to
1) make sure the files in the `svgs` folder are named appropriately - filenames should only have lowercase letters and underscores or dashes. Uppercase, numbers, or any other characters may result in final output files that do not work correctly.
1) run `python convert.py`
1) inspect the output file saved in the `clean` folder to ensure the process worked correctly
1) upload the files in the trash bags admin for the associated product mocks

You can tweak the files or script and re-run as many times as you need until the output is what you need.