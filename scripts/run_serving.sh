#!/bin/bash
# assuming already in docker bash?
echo Starting ModelServer
cd ..
tensorflow_model_server --port=8500 --model_name=saved_model --model_base_path=/model/