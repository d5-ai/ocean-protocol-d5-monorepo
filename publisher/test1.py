import os
import time
import uuid

from ocean_keeper.utils import get_account
from ocean_keeper.contract_handler import ContractHandler

from squid_py import Ocean, ConfigProvider, Config
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.agreements.service_agreement import ServiceAgreement

# keeper.path should point to the artifact folder which is assumed here to be the default path created by barge
config_dict = {'keeper-contracts':{
                    # Point to an Ethereum RPC client. Note that Squid learns the name of the network to work with from this client.
                    'keeper.url':'https://nile.dev-ocean.com',
                    # Specify the keeper contracts artifacts folder (has the smart contracts definitions json files). When you
                    # install the package, the artifacts are automatically picked up from the `keeper-contracts` Python
                    # dependency unless you are using a local ethereum network.
                    # 'keeper.path':'~/.ocean/keeper-contracts/artifacts',
                    'secret_store.url': 'https://secret-store.nile.dev-ocean.com',
                    'parity.url': 'https://nile.dev-ocean.com',
                    'parity.address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e',
                    'parity.password': 'node0',
                    'parity.address1': '0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0',
                    'parity.password1': 'secret',
                },
                'resources': {
                    # aquarius is the metadata store. It stores the assets DDO/DID-document
                    'aquarius.url': 'https://aquarius.marketplace.dev-ocean.com',
                    # Brizo is the publisher's agent. It serves purchase and requests for both data access and compute services
                    'brizo.url': 'https://brizo.marketplace.dev-ocean.com',
                    # points to the local database file used for storing temporary information (for instance, pending service agreements).
                    'storage.path': 'squid_py.db',
                    # Where to store downloaded asset files
                    'downloads.path': 'consume-downloads'
                }}

metadata = {
    "main": {
        "name": "Ocean protocol white paper 0",
        "dateCreated": "2012-02-01T10:55:11Z",
        "author": "Evgeny",
        "license": "CC0: Public Domain",
        "price": "0",
        "files": [
            {
                "index": 0,
                "contentType": "text/text",
                "checksum": str(uuid.uuid4()),
                "checksumType": "MD5",
                "contentLength": "12057507",
                "url": "https://raw.githubusercontent.com/oceanprotocol/barge/master/README.md"
            }
        ],
        "type": "dataset"
    }
}

ConfigProvider.set_config(Config('', config_dict))

ocean = Ocean()

print(ContractHandler.artifacts_path)

config = ocean.config

account = get_account(0) # use if env vars are declared
consumer_account = get_account(1) # PARITY_ADDRESS1 PARITY_KEYFILE1 & PARITY_PASSWORD1

#It is also possible to initialize account as follows bypassing the creation of environment variables
#account = Account(Web3.toChecksumAddress(address), pswrd, key_file, encr_key, key)

ddo = ocean.assets.create(metadata, account, providers=[])
assert ddo is not None, f'Registering asset on-chain failed.'
print("create asset success")

# Now we have an asset registered, we can verify it exists by resolving the did
_ddo = ocean.assets.resolve(ddo.did)
# ddo and _ddo should be identical
print(_ddo.did)