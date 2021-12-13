"""
Contains utility functions for the app
"""

import eth_utils
from web3 import Web3, HTTPProvider, WebsocketProvider
import json


def format_address(address):
    """
    Removes trailing 0's from an address
    Ethereum addresses are only 20 bytes long, 
    sometimes we receive an address with trailing 0's,
    :param address: address to format
    :type address: str
    :return: formatted address
    :type: str
    """
    bytes = eth_utils.to_bytes(address)

    # get the last 20 bytes only
    address_bytes = bytes[-20:]
    return eth_utils.to_checksum_address(address_bytes)
        

def instantiate_web3(url):
    """
    Web3 instance initializer
    :param url: url of the node
    :type url: str
    :return: Web3 instance
    :type: Web3
    """
    if isinstance(url, Web3):
        return url
    elif url.startswith('wss'):
        return Web3(WebsocketProvider(url, {"max_size": 10000000}))
    else:
        return Web3(HTTPProvider(url))


def fetch_abi(erc721=False):
    """
    Fetch ABI of a given contract, if it is verified
    Return default ABI, otherwise
    :param erc721: if the contract is ERC721
    :type erc721: bool
    :return: ABI of the contract
    :type: dict
    """
    if erc721:
        with open('app/abi/default-erc721.json') as abi:
            return json.load(abi)

    with open('app/abi/default-erc20.json') as abi:
        return json.load(abi)
