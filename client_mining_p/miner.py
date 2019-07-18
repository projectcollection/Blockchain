import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def valid_proof(last_proof, proof):
    guess_string = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess_string).hexdigest()

    return guess_hash[:6] == '000000'

def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof



if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        res = requests.get('http://localhost:5000/last_proof')
        last_proof = res.json()['last_proof']

        new_proof = proof_of_work(last_proof)

        mine_response = requests.post('http://localhost:5000/mine', json={'proof': new_proof,
                                                                    'id': 'some string',
                                                                    'wallet': 'wallet id' })
                                                                

        if mine_response.json()['message'] == 'success':
            coins_mined += 1
            print('total coins', str(coins_mined))
        
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
