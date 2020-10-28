usage: imgtools.exe [-h] [-v] [-r] [-s RESIZE [RESIZE ...]] [-ll LogLevel] path

Resize batches of images

positional arguments:
  path                  The path to the image file or folder containing image
                        files

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -r, --recursive       Recursively look for images in folders and subfolders
  -s RESIZE [RESIZE ...], --resize RESIZE [RESIZE ...]
                        Flag to enable the resize functionNew size can be
                        entered as a factor of the original image, for example
                        `-s 0.5` to resize images to half their size. It also
                        accepts specifying the width and height of the output
                        image: `-s 800 600` to resize all images to 800x600
                        pixels
  -ll LogLevel, --loglevel LogLevel
                        Select log level output. Valid values are:
                        CRITICAL,ERROR, WARNING, INFO, DEBUG, NOTSET

This application is intended to apply selected modifications to image files in
the selected folder. The output folder is selected in a new file explorer
window when image processing is finished.


Examples
--------
1. Resize all images in folder C:\Pictures\IMAGES to half the original size:
	imgtools.exe -p C:\Pictures\IMAGES -s 0.5

	2020-10-28 10:32:19 INFO     Log level set to: INFO
	2020-10-28 10:32:19 INFO     Source folder: C:\Pictures\IMAGES, recursive option disabled, new size=0.5x
	100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:00<00:00, 33.31it/s]
	2020-10-28 10:32:19 INFO     Finished processing 9 files in 0.29 seconds (32.68 msec/img)

2. Resize all images in folder C:\Pictures\IMAGES and subfolder to (800, 600):
	imgtools.exe -p C:\Pictures\IMAGES -r -s 800 600

	2020-10-28 10:33:07 INFO     Log level set to: INFO
	2020-10-28 10:33:07 INFO     Source folder: C:\Pictures\IMAGES, recursive option enabled, new size=(800, 600)
	100%|████████████████████████████████████████████████████████████████████████████████| 553/553 [00:31<00:00, 17.67it/s]
	2020-10-28 10:33:38 INFO     Finished processing 553 files in 31.32 seconds (56.64 msec/img)

	