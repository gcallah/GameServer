#!/bin/bash

USER=gcallah
DB = gamedb

if [ -z $DATA_DIR ]
then
    DATA_DIR=$(pwd)
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport

declare -a GameCollections=("games" )

for collection in ${GameCollections[@]}; do
    echo "Backing up $collection"
    $EXP --collection=$collection --db=$DB --out=$BKUP_DIR/$collection.json
done

cd $DATA_DIR; git commit $BKUP_DIR/*.json -m "Mongo DB backup"; git pull origin master; git push origin master
