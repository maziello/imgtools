# imgtools
Tool to process batches of images applying the same function to all of them.
Version 1.0 supports only resizing.

usage: imgtools [-h] [-v] [-r] [-f function [function ...]] [-ll LogLevel]
                path

Image processing in batches

positional arguments:
  path                  The path to the image file or folder containing image
                        files

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -r, --recursive       Recursively look for images in folders and subfolders
  -f function [function ...], --function function [function ...]
                        The function to process the image files and
                        corresponding arguments. For example `-f resize 0.5`
                        to resize images to half their size. It also accepts
                        specifying the width and height of the output image:
                        `-f resize 800 600` to resize all images to 800x600
                        pixels
  -ll LogLevel, --loglevel LogLevel
                        Select log level output. Valid values are:
                        CRITICAL,ERROR, WARNING, INFO, DEBUG, NOTSET

Examples
--------
1. Resize all images in folder C:\Pictures\IMAGES to half the original size:
	imgtools.exe -p C:\Pictures\IMAGES -f resize 0.5

	2020-10-27 23:57:36 INFO     Log level set to: INFO
	2020-10-27 23:57:36 INFO     Source folder: C:\Users\cmelus\Pictures\lot_evaluation\2014-06-11_09-56-35_ANA_HEp-2_204310_011921_JD_060514_A_(confirmed)\IMAGES\18_AMA, recursive option disabled, selected function: ['resize', '0.5']
	100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:00<00:00, 27.85it/s]
	2020-10-27 23:57:37 INFO     Finished processing 9 files in 0.35 seconds (38.56 msec/img)

2. Resize all images in folder C:\Pictures\IMAGES and subfolder to (800, 600):
	imgtools.exe -p C:\Pictures\IMAGES -r -f resize 800 600

	2020-10-27 23:58:21 INFO     Log level set to: INFO
	2020-10-27 23:58:21 INFO     Source folder: C:\Users\cmelus\Pictures\lot_evaluation\2014-06-11_09-56-35_ANA_HEp-2_204310_011921_JD_060514_A_(confirmed)\IMAGES, recursive option enabled, selected function: ['resize', '800', '600']
	100%|████████████████████████████████████████████████████████████████████████████████| 769/769 [00:40<00:00, 19.11it/s]
	2020-10-27 23:59:01 INFO     Finished processing 769 files in 40.27 seconds (52.37 msec/img)
