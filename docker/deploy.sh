#!/usr/bin/env bash
# -*- encoding UTF-8 -*-
# Author: Johny

export PGRDIR=$(cd `dirname $0`; pwd)
WORKSPACE=$PGRDIR
export VERSION=$1
source $WORKSPACE/env.sh

# only set VERSION if not set
[ -z "$VERSION" ] && VERSION=1.0

# break shell when fail
set -e

############################################################
# doing
############################################################
cd $PGRDIR && docker-compose -p $DOCKER_INSTANCE_NAME up -d

docker logs -f $DOCKER_INSTANCE_NAME