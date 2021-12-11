"""
This file defines classes for interacting with the blockchain.
It contains some useful functions for extracting data,
manipulating data and interacting with the blockchain.
"""
import csv
from app.utils import fetch_abi
from app.events import fetch_events

"""
A base abstract class that represents a Contract in Ethereum
Has ABI and address
This class is used to extract useful information from the contract
"""
class BaseContract:
    
    """
    Contract contstructor
    """
    def __init__(self, web3, address, abi, name=None, symbol=None):
        self.web3 = web3     
        self.address = address
        self.abi = abi
        self.name = name
        self.symbol = symbol

    def to_token_contract(self):
        """
        Converts the contract to a web3 contract
        """
        contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        return contract
    

"""
Class that represents an ERC20 token contract in Ethereum
"""
class ERC20Contract(BaseContract):
    
    """
    ERC20 Contract contstructor
    """
    def __init__(self, web3, address, abi=None, name=None, symbol=None):
        if abi:
            super().__init__(web3, address, abi, name, symbol)
        else:
            fetched_abi = fetch_abi(address, erc20=True)
            if fetched_abi:
                super().__init__(web3, address, abi=fetched_abi, name=name, symbol=symbol)
            else:
                raise Exception("Could not fetch ABI for contract at address {}".format(address))

    def get_transfers(self, from_block=0, to_block='latest'):
        """
        Get all transfers from the contract
        """
        pass
    
    def get_holders(self, from_block=0, to_block='latest'):
        """
        Get all holders of the contract
        """
        pass
        
    def fetch_transactions(self, from_block=0, to_block='latest'):
        """
        Fetch all Transfer events in the blockchain
        and save them to the csv file
        Infura only allows to fetch events in the span of 100 blocks
        Therefore, we need to fetch the events in batches
        and stop the loop when we have zero events in 1000 blocks
        """
        web3_contract = self.to_token_contract()
        
        if to_block == 'latest':
            to_block = self.web3.eth.block_number
        
        file_name = self.name if self.name is not None else self.address
        with open('app/data/{}.csv'.format(file_name), 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['from', 'to', 'value'])
            writer.writeheader()
            
            events = list(fetch_events(
                web3_contract.events.Transfer, 
                from_block=from_block, 
                to_block=to_block,
                address=self.address)
            )
            
            transactions_count = len(events)
            print("{} events found".format(transactions_count))
            
            writer.writerows(map(lambda event: event['args'], events))
            
            while True:
                to_block = from_block + 1
                from_block = to_block - 1000
                
                if from_block < 0:
                    break
                
                events = list(fetch_events(
                    web3_contract.events.Transfer, 
                    from_block=from_block, 
                    to_block=to_block,
                    address=self.address)
                )
                
                transactions_count = len(events)
                print('Inserting {} events'.format(transactions_count))
                writer.writerows(map(lambda event: event['args'], events))
                
                if transactions_count == 0:
                    break
            
    def __str__(self):
        return "ERC20 Contract: {}".format(self.address)
    

"""
Class that represents an ERC721 token contract in Ethereum
"""
class ERC721Contract(BaseContract):
    
    """
    ERC721 Contract contstructor
    """
    def __init__(self, web3, address, abi=None, name=None, symbol=None):
        if abi:
            super().__init__(web3, address, abi, name, symbol)
        else:
            fetched_abi = fetch_abi(address, erc721=True)
            if fetch_abi:
                super().__init__(web3, address, abi=fetched_abi, name=name, symbol=symbol)
            else:
                raise Exception("Could not fetch ABI for contract at address {}".format(address))
