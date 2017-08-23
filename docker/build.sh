#!/usr/bin/env bash
# -*- encoding UTF-8 -*-
# Author: Johny

export PGRDIR=$(cd `dirname $0`; pwd)
export WORKSPACE=$PGRDIR
export VERSION=$1

source $PGRDIR/env.sh

# only set VERSION if not set
[ -z "$VERSION" ] && VERSION=latest

# break shell when fail
set -e

# main release image
docker build -t $DOCKER_REGISTRY_URL/$DOCKER_IMAGE_NAME:$VERSION -f $PGRDIR/Dockerfile $WORKSPACE
