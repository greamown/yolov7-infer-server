import os, logging, json
from flask import Blueprint, send_from_directory, request
from common import error_msg, success_msg, save_file, NET, EVAL_PATH, SAVE_PATH

app_webapi = Blueprint( 'webapi', __name__)

@app_webapi.route("/")
def index():
    return "<h1>Hello! YOLOv7 inference</h1>"

@app_webapi.route('/infer', methods=['POST'])
def infer():
    # Get url
    print(request.environ)
    URL = "http://{}".format(request.environ['HTTP_HOST'])
    # Catch formdata
    error_info = save_file(request.files)
    if error_info:
        return error_msg(400, {}, str(error_info), log=True)
    # Inference
    NET.infer(source=EVAL_PATH, url = URL)

    return success_msg(200, {"results":NET.detections}, "Success")

@app_webapi.route('/show_result/<path:path>', methods=['GET'])
def show_result(path):
    img_path = os.path.join(SAVE_PATH, path)
    if os.path.exists(img_path):
        return send_from_directory(SAVE_PATH, path)
    else:
        return error_msg(400, {}, "This image does not exist:{}".format(img_path), log=True)