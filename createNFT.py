# this script is using for creating an NFT via Python code 

from cryptography.fernet import Fernet

from solana.keypair import Keypair
from solana.rpc.api import Client
import base58
import json
from base58 import b58decode,b58encode
from execution_engine import execute
from transactions import deploy
import metaplex_api


exported = '3Nq68xAVgKvwrig21CzuhtUYJLrRnN2GExBdeoWR8tXXGs84pPFGsQn78JQPhgUNfT9SEfESwFkvbLsgYmTQhuJu'
keypair = b58decode(exported)

privateKey = keypair[:32]
publicKey = keypair[32:]

api_endpoint = 'https://api.devnet.solana.com'
keys_dict = {}

keys_dict['api_endpoint'] = api_endpoint
keys_dict["descryption_key"] = Fernet.generate_key().decode("ascii")

keys_dict["source_account_secret_key"] = str(privateKey)
keys_dict["source_account_public_key"] = str(publicKey)

#print(publicKey)
#print(privateKey)
walletkeypair = Keypair.from_secret_key(privateKey)

#private_key = list(walletkeypair.secret_key)[:32]
keypair = Keypair(walletkeypair.public_key)
cipher = Fernet(keys_dict["descryption_key"])

cfg = {
    "PRIVATE_KEY": privateKey,
    "PUBLIC_KEY": publicKey,
    "DECRYPTION_KEY": keys_dict["descryption_key"] 
}

api = metaplex_api.MetaplexAPI(cfg)

metadataJson = 'https://raw.githubusercontent.com/nguyenson-kait/solanaDemo/main/mytest.json'

result = api.deploy(api_endpoint, "We are Cats !!", "Hellu Cats",5000)

contract_key = json.loads(result).get('contract')

mint_res = api.mint(api_endpoint, contract_key, publicKey, metadataJson)