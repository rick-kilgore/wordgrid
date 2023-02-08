#!/bin/bash

[ -f $HOME/.path.sh ] && . $HOME/.path.sh

rm -f main.py wordgrid.zip
cp gcloud.py main.py
zip wordgrid.zip requirements.txt *.py wwf.txt words.pickle
gcloud storage cp wordgrid.zip gs://wordgrid
rm -f main.py wordgrid.zip
gcloud functions deploy wordgrid --trigger-http --source gs://wordgrid/wordgrid.zip --entry-point http \
    --region us-west1 --runtime python310 --gen2 --allow-unauthenticated --memory 500MiB \
    --min-instances 10 --max-instances 20
