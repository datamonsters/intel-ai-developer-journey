from __future__ import print_function

import numpy as np
import tensorflow as tf

from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from keras.preprocessing import image


def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(400, 500))
    img = image.img_to_array(img)
    img = img / 255.
    img = np.expand_dims(img, axis=0)
    return img


def decode_prediction(proba):
    if proba > 0.5:
        return "Positive"
    else:
        return "Negative"


def get_prediction(image_path):
    
    image = preprocess_image(image_path)

    channel = implementations.insecure_channel("127.0.0.1", 9001)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = "emotions"
    request.model_spec.signature_name = "predict"

    request.inputs["images"].CopyFrom(
        tf.contrib.util.make_tensor_proto(image, shape=image.shape))

    result = stub.Predict(request, 10.0)
    prediction = np.array(result.outputs["scores"].float_val)[0]

    return [(decode_prediction(prediction), prediction)]