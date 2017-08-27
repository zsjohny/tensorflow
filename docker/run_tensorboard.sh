#!/usr/bin/env bash
# -*- encoding UTF-8 -*-
# Author: Johny

docker exec  -it tensorflow tensorboard --logdir=/tmp --port=6006
