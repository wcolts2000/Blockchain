import hashlib
import requests
from time import time

import sys
import json

coins = 0


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True).encode()
    proof = 0
    print(f'starting proof of work at time: {time()}, block_string: {block_string}')
    while not valid_proof(block_string, proof):
        proof += 1
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(f'finished proof: {proof} at time: {time()}, {guess_hash}')
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return True or False
    return guess_hash[:4] == "0000"


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        print(f"Requests: {r.json()}")
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        new_proof = proof_of_work(data.get('last_block'))

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        
        # add 1 to the number of coins mined and print it.  Otherwise,
        if 'message' in data:
            if data['message'] == 'New Block Forged':
                print(f'message: {data["message"]}')
                coins += 1
                print(f"Coins earned: {coins}")
            else:
                print(f"ERROR: {data['message']}")
        else:
            print(f"NOPE, {data}")
        # print the message from the server.
        pass


# CLASS EXAMPLE

# import hashlib
# import requests
# ​
# import sys
# import json
# ​
# ​
# def proof_of_work(block):
#     """
#     Simple Proof of Work Algorithm
#     Stringify the block and look for a proof.
#     Loop through possibilities, checking each one against `valid_proof`
#     in an effort to find a number that is a valid proof
#     :return: A valid proof for the provided block
#     """
#     # TODO: Make this work for miner
#     # One line version of code to stringify a block
#     block_string = json.dumps(block, sort_keys=True)
#     proof = 0
#     while valid_proof(block_string, proof) is False:
#         proof += 1
# ​
#     return proof
# ​
# ​
# def valid_proof(block_string, proof):
#     """
#     Validates the Proof:  Does hash(block_string, proof) contain 6
#     leading zeroes?  Return true if the proof is valid
#     :param block_string: <string> The stringified block to use to
#     check in combination with `proof`
#     :param proof: <int?> The value that when combined with the
#     stringified previous block results in a hash that has the
#     correct number of leading zeroes.
#     :return: True if the resulting hash is a valid proof, False otherwise
#     """
#     guess = f'{block_string}{proof}'.encode()
#     guess_hash = hashlib.sha256(guess).hexdigest()
#     return guess_hash[:6] == "000000"
# ​
# ​
# if __name__ == '__main__':
#     # What is the server address? IE `python3 miner.py https://server.com/api/`
#     if len(sys.argv) > 1:
#         node = sys.argv[1]
#     else:
#         node = "http://localhost:5000"
# ​
#     # Load ID
#     f = open("my_id.txt", "r")
#     id = f.read()
#     print("ID is", id)
#     f.close()
# ​
#     coins_mined = 0
# ​
#     # Run forever until interrupted
#     while True:
#         r = requests.get(url=node + "/last_block")
#         # Handle non-json response
#         try:
#             data = r.json()
#         except ValueError:
#             print("Error:  Non-json response")
#             print("Response returned:")
#             print(r)
#             break
# ​
#         # TODO: Get the block from `data` and use it to look for a new proof
#         new_proof = proof_of_work(data.get('last_block'))
# ​
#         # When found, POST it to the server {"proof": new_proof, "id": id}
#         post_data = {"proof": new_proof, "id": id}
# ​
#         r = requests.post(url=node + "/mine", json=post_data)
#         print(r)
#         data = r.json()
# ​
#         # TODO: If the server responds with a 'message' 'New Block Forged'
#         # add 1 to the number of coins mined and print it.  Otherwise,
#         # print the message from the server.
#         if data.get('message') == 'New Block Forged':
#             coins_mined += 1
#             print("Total coins mined: " + str(coins_mined))
#         else:
#             print(data.get('message'))