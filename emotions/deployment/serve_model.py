from __future__ import print_function

import os
import errno
import argparse

import tensorflow as tf
from keras.models import load_model
import keras.backend as K


def main(args):
	
	K.set_learning_phase(0)

	if not os.path.exists(args.model_path):
		raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.model_path)

	model = load_model(args.model_path)

	sess = K.get_session()

	export_path_base = os.path.dirname(args.model_path)
	export_version = args.model_version

	export_path = os.path.join(tf.compat.as_bytes(export_path_base),
							   tf.compat.as_bytes(str(export_version)))
	print('Exporting trained model to', export_path)
	
	builder = tf.saved_model.builder.SavedModelBuilder(export_path)

	model_input = tf.saved_model.utils.build_tensor_info(model.input)
	model_output = tf.saved_model.utils.build_tensor_info(model.output)

	prediction_signature = (tf.saved_model.signature_def_utils.build_signature_def(
								inputs={"images": model_input},
								outputs={"scores": model_output},
								method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

	legacy_init_op = tf.group(tf.tables_initializer(), name="legacy_init_op")

	builder.add_meta_graph_and_variables(sess, 
										 [tf.saved_model.tag_constants.SERVING],
										 signature_def_map={"predict": prediction_signature,},
										 legacy_init_op=legacy_init_op)

	builder.save()


if __name__ == "__main__":

	# argument parser from command line
    parser = argparse.ArgumentParser(add_help=True)

    # set of arguments to parse
    parser.add_argument("--model-path", 
                        type=str, 
                        required=True, 
                        help="path to model checkpoint")

    parser.add_argument("--model-version", 
                        type=int, 
                        default = 1, 
                        help="version of model")

    # parse arguments
    args = parser.parse_args()

    # launch experiment
    main(args)
