from flask import jsonify
import logging, os, shutil
from common import Yolov7
from werkzeug.utils import secure_filename

WEIGHTS = "model/yolov7.pt"
NET = Yolov7(WEIGHTS)
MAIN_PATH = "./data"
SAVE_PATH= os.path.join(MAIN_PATH, "results")
EVAL_PATH= os.path.join(MAIN_PATH, "eval")
ALLOWED_EXTENSIONS = {  "label":['txt', 'xml', 'json',
                                    "TXT", "XML", "JSON"],
                        "image":['png', 'jpg', 'jpeg', 'bmp', 
                                    "PNG", "JPG", "JPEG", "BMP"]
                    }

def error_msg(status:int, data:dict={}, text:str="", log=False):
    if log:
        logging.error(str(text))
    return response_content(status, data=data, text=text)

def success_msg(status:int, data:dict={}, text:str="", log=None):
    if log:
        logging.info(str(log))
    return response_content(status, data=data, text=text)

def response_content(status:int, data:dict={}, text:str=""):
    obj = {
            "status": status,
            "message":text,
            "data":data
        }
    return jsonify(obj), status

def clear_folder(folder):
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.mkdir(folder)

def save_file(files):
    # Clear old images
    clear_folder(EVAL_PATH)
    clear_folder(SAVE_PATH)
    # Create null list to collect images
    # img_list = []
    for key in files.keys():
        # Get files in files.getlist
        files = files.getlist(key)
        # Empty files
        if not files:
            msg = "No upload files."
            return msg
        # Get filename in files
        for idx, file in enumerate(files):
            # Most limit 10 pics
            if file and idx < 10:
                # Get file name
                filename = file.filename
                if "/" in file.filename:
                    filename = os.path.split(str(file.filename))[-1]
                filename = secure_filename(filename)
                # Skip other format exclude image format
                if not (filename.split(".")[-1] in ALLOWED_EXTENSIONS["image"]):
                    logging.error("This type of filename is not allowed:[{}:{}]".format(filename, filename.split(".")[-1]))
                    continue
                # Save image
                file.save(os.path.join(EVAL_PATH, filename))
                # img_path = os.path.join(EVAL_PATH, filename)
                # # Append to list
                # if os.path.exists(img_path):
                #     img_list.append(img_path)
            else:
                logging.error("Mostly 10 pics.")
    # return img_list