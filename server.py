import logging, sys
from common import logger
from initial import app
from webapi import app_webapi
from argparse import ArgumentParser, SUPPRESS
from waitress import serve

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-p', '--port', required=True, help = "Input port number")
    return parser

def main(args):
    app.register_blueprint(app_webapi)
    logging.info("Running webapi server...")
    # app.run(host="127.0.0.1", port=args.port, debug=False)
    serve(app, host="127.0.0.1", port=args.port)

if __name__ == '__main__':
    # Create log
    logger('./server.log', 'w', "info")
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)