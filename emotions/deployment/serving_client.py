import argparse

from utils import get_prediction


def main(args):

    prediction = get_prediction(args.image_path)
    print(prediction)


if __name__ == "__main__":

    # argument parser from command line
    parser = argparse.ArgumentParser(add_help=True)

    # set of arguments to parse
    parser.add_argument("--host", 
                        type=str, 
                        default="127.0.0.1", 
                        help="tf serving host address")

    parser.add_argument("--port", 
                        type=int, 
                        default=9001, 
                        help="tf serving host port")

    parser.add_argument("--image-path", 
                        type=str, 
                        required=True, 
                        help="image to classify")

    # parse arguments
    args = parser.parse_args()

    # launch classification
    main(args)
