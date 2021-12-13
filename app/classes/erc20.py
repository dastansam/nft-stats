import pandas as pd
from app.utils import fetch_abi
from app.ethereum import do_record_transactions, update_balances
from app.classes.base_contract import BaseContract
import os

"""
Class that represents an ERC20 token contract in Ethereum
"""
class ERC20Contract(BaseContract):
    
    """
    ERC20 Contract contstructor
    """
    def __init__(self, web3, address, abi=None, name=None, symbol=None, file_name=None):
        self.name = name
        self.symbol = symbol
        self.file_name = file_name
        
        if abi:
            super().__init__(web3, address, abi)
        else:
            fetched_abi = fetch_abi(erc20=True)
            if fetched_abi:
                super().__init__(web3, address, abi=fetched_abi)
            else:
                raise Exception("Could not fetch ABI for contract at address {}".format(address))
    
    def set_file_name(self):
        """
        Setter for the file name
        """
        name = self.name if self.name is not None else self.address[2:12]
        self.file_name = '{}_erc20_transactions'.format(name)
        
    def get_holders(self):
        """
        Get all holders of the contract
        This should always be called after the transactions are recorded
        """
        if self.file_name is not None:
            raise Exception("Transactions are not recorded yet")
        
        name = self.name if self.name is not None else self.address[2:12]
        possible_file_name = "{}_erc20_transactions.csv".format(name)
        
        if not os.path.isfile("app/data/{}".format(possible_file_name)):
            raise Exception("Transactions are not recorded yet")

        self.file_name = possible_file_name 
        
        transactions = pd.read_csv("app/data/{}".format(possible_file_name))
        
        # sort by block_number ascending
        transactions = transactions.sort_values(by=['block_number'], ascending=True)
        
        # extract unique addresses from from and to columns and add them to the holders dataframe
        addresses = set(transactions['from'].values).union(set(transactions['to'].values))
        
        print("Found {} unique addresses".format(len(addresses)))
        
        # populate with 0 balance
        holders = {address: {'address': address, 'balance': 0} for address in addresses}
        
        holders = update_balances(holders, transactions)
        
        holders = pd.DataFrame(list(holders.values()))
        
        holders.to_csv("app/data/{}_holders.csv".format(self.name), index=False)

    def record_transactions(self, from_block=0, to_block='latest'):
        """
        Fetch all Transfer events in the blockchain
        and save them to the csv file
        """
        web3_contract = self.to_token_contract()
        
        if to_block == 'latest':
            to_block = self.web3.eth.block_number
        
        self.set_file_name()
        
        do_record_transactions(
            self.address, 
            web3_contract,
            self.file_name,
            initial_from_block=from_block, 
            initial_to_block=to_block
        )
     
    def __str__(self):
        return "ERC20 Contract: {}".format(self.address)
