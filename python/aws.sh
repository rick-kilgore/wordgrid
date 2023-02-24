#!/bin/bash

[ -f $HOME/.path.sh ] && . $HOME/.path.sh

zip wordgrid.zip requirements.txt *.py wwf.txt words.pickle
if [ "$1" = "-i" ]; then
  aws lambda create-function --function-name wordgrid --zip-file fileb://wordgrid.zip \
      --role arn:aws:iam::251183135174:role/lambda-wordgrid --runtime python3.9 \
      --handler aws.handle_findwords --timeout 60
else
  aws lambda update-function-code --function-name wordgrid --zip-file fileb://wordgrid.zip
fi
rm -f wordgrid.zip
