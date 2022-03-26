from decimal import Clamped
import transactions
from solana.publickey import PublicKey
import solana.rpc.api
import base58
from base58 import b58decode,b58encode
from solana.rpc.types import TokenAccountOpts 
import struct
import base64

def get_metadata_account(mint_key):
    return PublicKey.find_program_address(
        [b'metadata', bytes(METADATA_PROGRAM_ID), bytes(PublicKey(mint_key))],
        METADATA_PROGRAM_ID
    )[0]

def unpack_metadata_account(data):
    assert(data[0] == 4)
    i = 1
    source_account = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    mint_account = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    name_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    name = struct.unpack('<' + "B"*name_len, data[i:i+name_len])
    i += name_len
    symbol_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4 
    symbol = struct.unpack('<' + "B"*symbol_len, data[i:i+symbol_len])
    i += symbol_len
    uri_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4 
    uri = struct.unpack('<' + "B"*uri_len, data[i:i+uri_len])
    i += uri_len
    fee = struct.unpack('<h', data[i:i+2])[0]
    i += 2
    has_creator = data[i] 
    i += 1
    creators = []
    verified = []
    share = []
    if has_creator:
        creator_len = struct.unpack('<I', data[i:i+4])[0]
        i += 4
        for _ in range(creator_len):
            creator = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
            creators.append(creator)
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    metadata = {
        "update_authority": source_account,
        "mint": mint_account,
        "data": {
            "name": bytes(name).decode("utf-8").strip("\x00"),
            "symbol": bytes(symbol).decode("utf-8").strip("\x00"),
            "uri": bytes(uri).decode("utf-8").strip("\x00"),
            "seller_fee_basis_points": fee,
            "creators": creators,
            "verified": verified,
            "share": share,
        },
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    return metadata
api_endpoint="https://api.devnet.solana.com/"
nftAddress = 'Ein6KfzpfxcwQvd8VthvFE3BxWgj74eSmUE7tDRZNtHm'


exported = '3Nq68xAVgKvwrig21CzuhtUYJLrRnN2GExBdeoWR8tXXGs84pPFGsQn78JQPhgUNfT9SEfESwFkvbLsgYmTQhuJu'
keypair = b58decode(exported)

privateKey = keypair[:32]
publicKey = keypair[32:]

# All NFTs from account
client = solana.rpc.api.Client(api_endpoint)
res = client.get_account_info(PublicKey(publicKey))
#print(res)
METADATA_PROGRAM_ID = PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')
TOKEN_PROGRAM_ID = PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
opts = TokenAccountOpts(program_id = TOKEN_PROGRAM_ID, encoding= 'jsonParsed')

#res = client.get_account_info(PublicKey(publicKey))
#print(client.get_token_accounts_by_owner(PublicKey(publicKey),opts))
#Json of NFT
metadata_account = get_metadata_account(nftAddress)

decoded_data = base64.b64decode(client.get_account_info(metadata_account)['result']['value']['data'][0])

print(decoded_data[0])

metadata = unpack_metadata_account(decoded_data)

print(metadata)
