#!/usr/bin/env bash
# -*- encoding UTF-8 -*-
# Author: Johny

export PGRDIR=$(cd `dirname $0`; pwd)
export WORKSPACE=$PGRDIR/../
export VERSION=$1

source $PGRDIR/env.sh

# only set VERSION if not set
[ -z "$VERSION" ] && VERSION=latest

echo pull image $VERSION
docker pull $DOCKER_REGISTRY_URL/$DOCKER_IMAGE_NAME:$VERSION
