#! /bin/bash
# Command can be either get-mev or inspect-mev
# Block is the block number
# Example: ./test_mev_server.sh get-mev 16379709
# Don't forget to chmod it :)
COMMAND="$1"
START_BLOCK="$2"
END_BLOCK="$3"
echo $COMMAND $START_BLOCK $END_BLOCK
curl -H 'Content-Type: application/json' \
	-d "{ \"start_block\":\"$START_BLOCK\",\"end_block\":\"$END_BLOCK\"}" \
	-X POST \
	"http://test.xtreamly.io:7321/$COMMAND"
