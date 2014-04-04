#!/bin/bash
#
#   on-download-complete.sh
#
#   $ export ARIA2CLIB_HOME=".../aria2c-as-a-service"
GID=$1
FILES=$2
FILEPATH=${@:3}

python ${ARIA2CLIB_HOME}/aria2clib event \
    --handler=${ARIA2CLIB_HOME}/tests/handlers/on-download-complete.py \
    --gid=$GID --files=$FILES --path="$FILEPATH"

