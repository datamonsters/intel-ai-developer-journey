#!/bin/bash

sudo docker run -d -v /home/johndoe:/root/shared -p 9000:9000 -p 8888:8888 emotions
