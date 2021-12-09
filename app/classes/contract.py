"""
This file defines classes for interacting with the blockchain.
It contains some useful functions for extracting data,
manipulating data and interacting with the blockchain.
"""
import web3
import requests
from web3.main import Web3
from app.config import ETHERSCAN_API_KEY
from app.utils import fetch_abi

"""
A base abstract class that represents a Contract in Ethereum
Has ABI and address
This class is used to extract useful information from the contract
"""
class BaseContract:
    
    """
    Contract contstructor
    """
    def __init__(self, address, abi, name=None, symbol=None):        
        self.address = address
        self.abi = abi
        self.name = name
        self.symbol = symbol

    def to_web3_contract(self):
        """
        Converts the contract to a web3 contract
        """
        contract = Web3.eth.contract(address=self.address, abi=self.abi)
        return contract
    

"""
Class that represents an ERC20 token contract in Ethereum
"""
class ERC20Contract(BaseContract):
    
    """
    ERC20 Contract contstructor
    """
    def __init__(self, address, abi=None, name=None, symbol=None):
        if abi:
            super.__init__(self, address, abi, name, symbol)
        else:
            fetched_abi = fetch_abi(address, erc20=True)
            if fetched_abi:
                super.__init__(self, address, fetched_abi, name, symbol)
            else:
                raise Exception("Could not fetch ABI for contract at address {}".format(address))

    def get_transfer(from_block=0, to_block='latest'):
        """
        Get all transfers from the contract
        """
        pass
    
    def get_holders(from_block=0, to_block='latest'):
        """
        Get all holders of the contract
        """
        pass
    
    def __str__(self):
        return "ERC20 Contract: {}".format(self.address)
    

"""
Class that represents an ERC721 token contract in Ethereum
"""
class ERC721Contract(BaseContract):
    
    """
    ERC721 Contract contstructor
    """
    def __init__(self, address, abi=None, name=None, symbol=None):
        if abi:
            super.__init__(self, address, abi, name, symbol)
        else:
            fetched_abi = fetch_abi(address, erc721=True)
            if fetch_abi:
                super.__init__(self, address, fetched_abi, name, symbol)
            else:
                raise Exception("Could not fetch ABI for contract at address {}".format(address))

