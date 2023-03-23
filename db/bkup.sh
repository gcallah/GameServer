#!/bin/bash

USER=gcallah
DB = gamedb

GAME_CONNECT_STR='mongodb+srv://serverlessinstance0.irvgp.mongodb.net/DB?authSource=admin'

if [ -z $DATA_DIR ]
then
    DATA_DIR=$(pwd)
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport

if [ -z $GAME_MONGO_PW ]
then
    echo "You must set GAME_MONGO_PW in your env before running this script."
    exit 1
fi

declare -a GameCollections=("games" )

for collection in ${GameCollections[@]}; do
    echo "Backing up $collection"
    $EXP --authenticationDatabase=admin --collection=$collection --db=$DB --out=$BKUP_DIR/$collection.json $GAME_CONNECT_STR --username $USER --password $GAME_MONGO_PW
done

cd $DATA_DIR; git commit $BKUP_DIR/*.json -m "Mongo DB backup"; git pull origin master; git push origin master
