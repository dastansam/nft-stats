import eth_utils
from web3 import Web3, HTTPProvider, WebsocketProvider
import json
import requests
from app.config import ETHERSCAN_API_KEY


def format_address(address):
    """
    Removes trailing 0's from an address
    Ethereum addresses are only 20 bytes long, 
    sometimes we receive an address with trailing 0's,
    """
    bytes = eth_utils.to_bytes(address)

    # get the last 20 bytes only
    address_bytes = bytes[-20:]
    return eth_utils.to_checksum_address(address_bytes)
        

def instantiate_web3(url):
    """
    Web3 initializer
    """
    if isinstance(url, Web3):
        return url
    elif url.startswith('wss'):
        return Web3(WebsocketProvider(url))
    else:
        return Web3(HTTPProvider(url))


def fetch_abi(address, erc20=False, erc721=False):
    """
    Fetch ABI of a given contract, if it is verified
    Return default ABI, otherwise
    """
    url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={ETHERSCAN_API_KEY}'
    abi_fetch = requests.get(url)
    
    if abi_fetch.status_code == 200:
        response_json = abi_fetch.json()
        abi_json = json.loads(response_json['result'])
        return abi_json
    
    else:
        if erc20:
            with open('app/abi/default-erc20.json') as abi:
                return json.load(abi)
        
        elif erc721:
            with open('app/abi/default-erc721.json') as abi:
                return json.load(abi)
    
    return None
