from solana.keypair import Keypair
from solana.rpc.api import Client
import base58
import json
from base58 import b58decode,b58encode
from execution_engine import execute
from transactions import deploy
import metaplex_api
import array
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
exported = '3Nq68xAVgKvwrig21CzuhtUYJLrRnN2GExBdeoWR8tXXGs84pPFGsQn78JQPhgUNfT9SEfESwFkvbLsgYmTQhuJu'
keypair = b58decode(exported)

privateKey = keypair[:32]
publicKey = keypair[32:]
walletkeypair = Keypair.from_secret_key(privateKey)

toWalletAddress = 'BntZT1ASu3beFsWkjWNhiE7FqLRrGNhn7RzRqTk8UyBC'
solana_client = Client("https://api.devnet.solana.com/")

fee = solana_client.get_fees()['result']['value']['feeCalculator']['lamportsPerSignature']

json.load
LAMPORTPERSOL = 1000000000
txn = Transaction().add(transfer(TransferParams(from_pubkey=walletkeypair.public_key, to_pubkey=toWalletAddress, lamports=(int)(LAMPORTPERSOL*0.5 - fee))))
solana_client.send_transaction(txn, walletkeypair)