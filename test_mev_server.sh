#! /bin/bash
# Command can be either get-mev or inspect-mev
# Block is the block number
# Example: ./test_mev_server.sh get-mev 16379709
# Don't forget to chmod it :)
COMMAND="$1"
BLOCK="$2"
echo $COMMAND $BLOCK
curl -H 'Content-Type: application/json' \
	-d "{ \"block\":\"$BLOCK\",\"body\":\"bar\", \"id\": 1}" \
	-X POST \
	"http://test.xtreamly.io:7321/$COMMAND"
