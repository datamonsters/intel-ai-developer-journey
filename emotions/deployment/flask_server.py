from __future__ import print_function

import argparse

from flask import Flask
from flask import request
from flask import jsonify

from utils import get_prediction


application = Flask(__name__)


@application.route("/predict", methods=["POST"])
def predict():
    if request.files.get("data"):
        img = request.files["data"]
        resp = get_prediction(img)
        resp = jsonify(resp)
        return resp
    else:
        return jsonify({"status": "error"})


if __name__ == "__main__":

    # argument parser from command line
    parser = argparse.ArgumentParser(add_help=True)

    # set of arguments to parse
    parser.add_argument("--port", 
                        type=int, 
                        required=True, 
                        help="port to run flask server")

    # parse arguments
    args = parser.parse_args()

    # launch flask server accessible from all hosts
    application.run(port=args.port, host="0.0.0.0")

