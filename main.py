import datetime
import os
import logging
import sys
from tqdm import tqdm
from cv2 import resize as cvresize, imread, imwrite
import argparse
import subprocess

"""
usage: main.py [-h] [-v] [-r] [-s RESIZE [RESIZE ...]] [-ll LogLevel] path

Resize batches of images
This application is intended to apply selected modifications to image files in
 the selected folder. The output folder is selected in a new file explorer 
 window when image processing is finished.

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
"""

__version__ = "1.0"


def setup_logger(name,
                 output_folder,
                 log_file_name,
                 selected_log_level=20):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    filehandler = logging.FileHandler(os.path.join(output_folder,
                                                   log_file_name), mode='w')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    filehandler.setFormatter(formatter)
    screen_handler.setFormatter(formatter)
    thislogger = logging.getLogger(name)
    thislogger.setLevel(selected_log_level)
    thislogger.addHandler(filehandler)
    thislogger.addHandler(screen_handler)
    return thislogger


def resize(image, new_size):
    if isinstance(image, str):
        if os.path.isfile(image):
            image = imread(image)
        else:
            raise FileNotFoundError(f"Can't open file {image}")

    if isinstance(new_size, float):
        return cvresize(image, (int(image.shape[1] * new_size),
                                int(image.shape[0] * new_size)))

    return cvresize(image, new_size)


output_log_folder = os.getcwd()
loglevels = {'CRITICAL': 50,
             'ERROR': 40,
             'WARNING': 30,
             'INFO': 20,
             'DEBUG': 10,
             'NOTSET': 0}

my_parser = argparse.ArgumentParser(
    description='Resize batches of images',
    epilog='This application is intended to apply selected modifications to '
           'image files in the selected folder. The output folder is selected '
           'in a new file explorer  window when image processing is finished.')

my_parser.add_argument('-v',
                       '--version',
                       action='version',
                       version=f'%(prog)s version {__version__}')

my_parser.add_argument('path',
                       metavar='path',
                       type=str,
                       help='The path to the image file or '
                            'folder containing image files')

my_parser.add_argument('-r',
                       '--recursive',
                       # metavar='recursive',
                       # type=bool,
                       action='store_true',
                       help='Recursively look for images in folders and '
                            'subfolders',
                       required=False)

my_parser.add_argument('-s',
                       '--resize',
                       dest='resize',
                       # metavar='resize',
                       nargs='+',
                       action='store',
                       help='Flag to enable the resize function'
                            'New size can be entered as a factor of the '
                            'original image, for example `-s 0.5` to resize '
                            'images to half their size. '
                            'It also accepts specifying the width and height '
                            'of the output image: `-s 800 600` to '
                            'resize all images to 800x600 pixels',
                       required=False,
                       default=[0.5])

my_parser.add_argument('-ll',
                       '--loglevel',
                       metavar='LogLevel',
                       type=str.upper,
                       choices=list(loglevels.keys()),
                       help='Select log level output. Valid values are: '
                            'CRITICAL,ERROR, WARNING, INFO, DEBUG, NOTSET',
                       default='INFO',
                       required=False)

args = my_parser.parse_args()

source_path = args.path
resizefn = args.resize
log_level_desc = args.loglevel
recursive = args.recursive

log_level = loglevels[log_level_desc]
log_msg = f"Log level set to: {log_level_desc}"
now = datetime.datetime.now()

logger = setup_logger('imgtools_log', output_log_folder,
                      f"imgtools_{now.year}_{now.month:02d}_{now.day:02d}.log",
                      log_level)

logger.info(log_msg)


if resizefn:
    if len(resizefn) == 1:
        new_size = float(resizefn[0])
    if len(resizefn) == 2:
        new_size = tuple([int(v) for v in resizefn[0:2]])

logger.info(f"Source folder: {source_path}, recursive option "
            f"{'enabled' if recursive else 'disabled'}, "
            f"new size="
            f"{str(new_size) if isinstance(new_size, tuple) else str(new_size)+'x'}")

logger.debug(f"Resize: {resizefn}, "
             f"newsize={new_size if len(resizefn) > 1 else None}")

file_filter = ('jpg', 'tif', 'png', 'webp')

files = [os.path.normpath(os.path.join(root, f))
         for root, dirs, files in os.walk(source_path)
         for f in files if any(x in f for x in file_filter)] \
    if recursive else \
    [os.path.join(source_path, f) for f in os.listdir(source_path)
     if any(x in f for x in file_filter)]

output_folder = os.path.join(source_path, 'resized')
logger.debug(f"Output folder= {output_folder}, "
             f"exists={os.path.isdir(output_folder)}")
if not os.path.isdir(output_folder):
    os.makedirs(output_folder)
    logger.debug(f"{'folder created' if os.path.isdir(output_folder) else 'Folder creation failed'}")

t0 = datetime.datetime.now()
for file in tqdm(files):
    img = imread(file)
    # if process == 'resize':
    output = resize(img, new_size)
    original_filename = os.path.basename(file)
    output_filename = f"{original_filename.split('.')[0]}_resized." \
                      f"{original_filename.split('.')[1]}"
    imwrite(os.path.join(output_folder, output_filename), output)

t1 = datetime.datetime.now()
logger.info(f"Finished processing {len(files)} files "
            f"in {(t1 - t0).total_seconds():.2f} seconds "
            f"({(t1 - t0).total_seconds()/len(files)*1000:.2f} msec/img)")

logger.info(f"Processed images can be found in folder:"
            f" {output_folder}")
subprocess.Popen(f'explorer /select, {output_folder}')
