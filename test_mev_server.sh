#! /bin/bash
COMMAND="$1"
BLOCK="$2"
echo $COMMAND $BLOCK
curl -H 'Content-Type: application/json' \
	-d "{ \"block\":\"$BLOCK\",\"body\":\"bar\", \"id\": 1}" \
	-X POST \
	"http://test.xtreamly.io:7321/$COMMAND"
