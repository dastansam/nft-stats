from web3 import Web3, HTTPProvider
import json
import requests
from config import ETHERSCAN_API_KEY


def instantiate_web3(url):
    """
    Web3 initializer
    """
    if isinstance(url, Web3):
        return url
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
        abi = abi_fetch.json()['result']
        return abi
    
    if erc20:
        with open('../abi/default-erc20.json') as abi:
            return json.load(abi)
    
    elif erc721:
        with open('../abi/default-erc721.json') as abi:
            return json.load(abi)
    
    return None


def get_logs(contract, event_type, start_block=0, end_block='latest'):
    """
    Get logs of a given contract
    """
    contract.get_past_events(event_type,)
    