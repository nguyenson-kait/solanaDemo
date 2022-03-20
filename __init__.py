import transactions
import array
from solana.keypair import Keypair 
from base58 import b58decode,b58encode
from execution_engine import execute

exported = '3Nq68xAVgKvwrig21CzuhtUYJLrRnN2GExBdeoWR8tXXGs84pPFGsQn78JQPhgUNfT9SEfESwFkvbLsgYmTQhuJu'
keypair = b58decode(exported)

privateKey = keypair[:32]
publicKey = keypair[32:]

print(publicKey)
print(b58encode(privateKey).decode())

walletkeypair = Keypair.from_secret_key(privateKey)
#walletkeypair = Keypair.from_seed('')
nftAddress = '5JfkGC6J9RB7CHn1i1ML8N5boX37ySjAwUvcsPeUF2KS'

api_endpoint="https://api.devnet.solana.com/"
data = {'name': "New name","symbol" : "New symbol"}

#print(data['name'])
#print('Public key:' + str(b58encode(publicKey).decode()) + 'len = ' + str(len(publicKey)))
#print('Private key' + str(b58encode(privateKey).decode()) + 'len = ' + str(len (privateKey)))
resp = {}

# while 'result' not in resp:
tx, signers = transactions.update_token_metadata(api_endpoint,walletkeypair,nftAddress,"https://raw.githubusercontent.com/nguyenson-kait/solanaDemo/main/mytest.json",data,10000,[b58encode(publicKey).decode()],b58encode(privateKey).decode(),[100])
print("tx:", tx)
resp = execute(
                api_endpoint,
                tx,
                signers,
                max_retries=3,
                skip_confirmation=True,
                max_timeout=60,
                target=20,
                finalized=True,
            )
print(b58encode(str(walletkeypair.public_key)).decode())

#transactions.update_token_metadata('')