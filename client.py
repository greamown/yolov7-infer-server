import logging, sys, os, requests
from argparse import ArgumentParser, SUPPRESS
IP = "127.0.0.1"
PORT = "550"

def logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    basic_formatter = logging.Formatter( "%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)", "%y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler('client.log', 'w', 'utf-8')
    file_handler.setFormatter(basic_formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-p', '--path', required=True, help = "The path of inference images. you can input the folder path or the image path.")
    return parser

def upload_images(file_list):
    url = "http://{}:{}/infer".format(IP, PORT)
    files = []
    for file in file_list:
        fileobj = open(file, 'rb')
        files.append(('files', (file, fileobj, 'image/jpeg')))
    res = requests.request("POST", url, files=files)
    return res

def main(args):
    # Check type of path
    if os.path.isdir(args.path):
        file_list = [ os.path.join(args.path, file) for file in os.listdir(args.path)]
        result = upload_images(file_list)
        if "4" in str(result.status_code):
            logging.error("Upload files status:{}".format(result.status_code))
        elif "2" in str(result.status_code):
            logging.info(str(result.json()["data"]))
    elif os.path.isfile(args.path):
        file_list = [ args.path ]
        result = upload_images(file_list)
        if "4" in str(result.status_code):
            logging.error("Upload files status:{}".format(result.status_code))
        elif "2" in str(result.status_code):
            logging.info(str(result.json()["data"]))
    else:
        logging.error("This path does not exist:[{}]".format(args.path))
    
if __name__ == '__main__':
    logger()
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)