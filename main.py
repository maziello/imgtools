import datetime
import os
import logging
# import pathlib
import sys
from tqdm import tqdm
# from PIL import Image
from cv2 import resize as cvresize, imread, imwrite
import argparse

"""
This application is intended to apply selected modifications to image files in
 the selected folder

Usage:
imgtools.py <input file/folder> <log level>

  <input file/folder>   Input image file to parse. If it is a folder, all 
                        image files in the folder will be processed.

  <log level>           Define the minimum log level to output on screen and
                        the log file. Options are: 
                        CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
                        The default value is INFO
  -h --help     Show this screen.
  --version     Show version.
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
    # if isinstance(image, (str, pathlib.Path)):
    if isinstance(image, str):
        if os.path.isfile(image):
            # image = Image.open(image)
            image = imread(image)
        else:
            raise FileNotFoundError(f"Can't open file {image}")

    if isinstance(new_size, float):
        # return image.resize((int(image.width * new_size),
        #                      int(image.height * new_size)))
        return cvresize(image, (int(image.shape[1] * new_size),
                                int(image.shape[0] * new_size)))

    # return image.resize(new_size)
    return cvresize(image, new_size)


# output_log_folder = os.path.expanduser('~\\Documents')
output_log_folder = os.getcwd()
loglevels = {'CRITICAL': 50,
             'ERROR': 40,
             'WARNING': 30,
             'INFO': 20,
             'DEBUG': 10,
             'NOTSET': 0}

my_parser = argparse.ArgumentParser(prog='imgtools',
                                    description='Image processing in batches')

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

my_parser.add_argument('-f',
                       '--function',
                       metavar='function',
                       nargs='+',
                       type=str,
                       help='The function to process the image files and '
                            'corresponding arguments. '
                            'For example `-f resize 0.5` to resize images to '
                            'half their size. '
                            'It also accepts specifying the width and height '
                            'of the output image: `-f resize 800 600` to '
                            'resize all images to 800x600 pixels',
                       required=False,
                       default=['resize', '0.5'])

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
function = args.function
log_level_desc = args.loglevel
recursive = args.recursive

log_level = loglevels[log_level_desc]
log_msg = f"Log level set to: {log_level_desc}"
now = datetime.datetime.now()

logger = setup_logger('imgtools_log', output_log_folder,
                      f"imgtools_{now.year}_{now.month:02d}_{now.day:02d}",
                      log_level)

logger.info(log_msg)

logger.info(f"Source folder: {source_path}, recursive option "
            f"{'enabled' if recursive else 'disabled'}, selected function: "
            f"{function}")

process = function[0]
if len(function) == 2:
    new_size = float(function[1])
if len(function) == 3:
    new_size = tuple([int(v) for v in function[1:3]])

logger.debug(f"Function: {process}, "
             f"newsize={new_size if len(function) > 1 else None}")

file_filter = ('jpg', 'tif', 'png', 'webp')

files = [os.path.normpath(os.path.join(root, f))
         for root, dirs, files in os.walk(source_path)
         for f in files if any(x in f for x in file_filter)] \
    if recursive else \
    [os.path.join(source_path, f) for f in os.listdir(source_path)
     if any(x in f for x in file_filter)]

output_folder = os.path.join(source_path, 'resized')
logger.debug(f"Output folder= {output_folder}, exists= {os.path.isdir(output_folder)}")
if not os.path.isdir(output_folder):
    os.makedirs(output_folder)
    logger.debug(f"{'folder created' if os.path.isdir(output_folder) else 'Folder creation failed'}")

t0 = datetime.datetime.now()
for file in tqdm(files):
    # with Image.open(file) as img:
    img = imread(file)
    if process == 'resize':
        output = resize(img, new_size)
        original_filename = os.path.basename(file)
        output_filename = f"{original_filename.split('.')[0]}_resized." \
                          f"{original_filename.split('.')[1]}"
    # output.save(os.path.join(output_folder, output_filename))
    imwrite(os.path.join(output_folder, output_filename), output)

    # logger.info(f"file "
    #             f"{file if len(file) <=30 else f'...{os.path.basename(file)}'}"
    #             f" processed")

t1 = datetime.datetime.now()
logger.info(f"Finished processing {len(files)} files "
            f"in {(t1 - t0).total_seconds():.2f} seconds "
            f"({(t1 - t0).total_seconds()/len(files)*1000:.2f} msec/img)")
