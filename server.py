from sanic import Sanic, response
from sanic.log import logger
import json
import subprocess
import asyncpg

CONNECTION = "postgresql://postgres:postgres@localhost:5432/mev_inspect"
app = Sanic(__name__)

@app.route('/inspect-mev', methods=['POST'])
async def inspect_mev(request):
    # Assuming the request contains data to be passed to the shell command
    data = request.json  # Assuming JSON data is sent in the request
    if data is None:
        return response.json({'message': 'No JSON data provided in the request'}, status=400)

    # Assuming the command to be executed is 'ls' for demonstration purposes
    # command = ['cd ../mev-inspect-py; poetry run inspect-block 16379706']  # Replace 'ls' with the actual command you want to run
    command = [f'cd ../mev-inspect-py && poetry run inspect-block {data["block"]}']  # Replace 'ls' with the actual command you want to run

    try:
        # Run the shell command
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            # Command executed successfully
            return response.json({'output': result.stdout})
        else:
            # Command failed
            return response.json({'error': result.stderr}, status=500)
    except Exception as e:
        return response.json({'error': str(e)}, status=500)

@app.route('/get-mev', methods=['POST'])
async def get_mev(request):

    # Assuming the request contains data to be passed to the shell command
    data = request.json  # Assuming JSON data is sent in the request
    if data is None:
        return response.json({'message': 'No JSON data provided in the request'}, status=400)

    try:
        block_number = int(data["block"])
        logger.info(block_number)

        conn = await asyncpg.connect(CONNECTION)

        arbitrages_records = await conn.fetch("SELECT transaction_hash FROM arbitrages WHERE block_number = $1;", block_number)
        sandwiches_records = await conn.fetch("SELECT frontrun_swap_transaction_hash, backrun_swap_transaction_hash FROM sandwiches WHERE block_number = $1;", block_number)

        logger.info(f"Arbitrages: {arbitrages_records}")
        logger.info(f"Sandwiches: {sandwiches_records}")
        arbitrages = [dict(arbitrage) for arbitrage in arbitrages_records]
        sandwiches = [dict(sandwich) for sandwich in sandwiches_records]

        await conn.close()
        return response.json({'arbitrages': json.dumps(arbitrages), 'sandwiches': json.dumps(sandwiches)})

    except Exception as e:
        return response.json({'error': str(e)}, status=500)

@app.route('/get-mevs', methods=['POST'])
async def get_mevs(request):

    # Assuming the request contains data to be passed to the shell command
    data = request.json  # Assuming JSON data is sent in the request
    if data is None:
        return response.json({'message': 'No JSON data provided in the request'}, status=400)

    try:
        start_block = int(data["start_block"])
        end_block = int(data["end_block"])
        logger.info(f"From {start_block} to {end_block}")

        conn = await asyncpg.connect(CONNECTION)

        arbitrages_records = await conn.fetch("SELECT transaction_hash FROM arbitrages WHERE block_number >= $1 and block_number <= $2;", start_block, end_block)
        sandwiches_records = await conn.fetch("SELECT frontrun_swap_transaction_hash, backrun_swap_transaction_hash FROM sandwiches WHERE block_number <= $1 and block_number >= $2;", start_block , end_block)

        logger.info(f"Arbitrages: {arbitrages_records}")
        logger.info(f"Sandwiches: {sandwiches_records}")
        arbitrages = [dict(arbitrage) for arbitrage in arbitrages_records]
        sandwiches = [dict(sandwich) for sandwich in sandwiches_records]

        await conn.close()
        return response.json({'arbitrages': json.dumps(arbitrages), 'sandwiches': json.dumps(sandwiches)})

    except Exception as e:
        return response.json({'error': str(e)}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7321)
