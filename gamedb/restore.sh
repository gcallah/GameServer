#!/bin/sh

# Restores our prod DB to your local mongo instance.

export LOCAL_MONGO=1
BKUP_DIR=bkup
IMP=/usr/local/bin/mongoimport

declare -a APICollections=("categories" "APIs" "countries" "states" "api_stats" "queries" "reports" "report_destinations")

for collection in ${APICollections[@]}; do
    echo "Restoring $collection"
    $IMP --db gamedb --collection $collection --drop --file $BKUP_DIR/$collection.json
done
