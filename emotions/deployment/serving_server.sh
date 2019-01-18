#!/bin/bash

tensorflow_model_server --port=9001 --enable-batching=true --model_name="emotions" --model_base_path="../models" &> emotions.log &
