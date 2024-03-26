#!/bin/sh
export ID=
export HOST1=
export HOST2=
export PYTHON=/usr/local/bin/python3
export TEMP1=temp1.json
export TEMP2=temp2.json
rm $TEMP2 2> /dev/null
usacloud dns read $ID --query '.[0].Records' > $TEMP1
$PYTHON usacloud-ddns.py $HOST1 $HOST2
if [ -f ./$TEMP2 ]; then
  export JSON=`cat $TEMP2`
  usacloud dns update $ID --assumeyes --parameters "$JSON"
fi