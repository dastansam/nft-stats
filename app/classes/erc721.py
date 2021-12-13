import pandas as pd
from app.classes.base_contract import BaseContract
from app.utils import fetch_abi
from app.ethereum import do_record_transactions, update_balances

"""
Class that represents an ERC721 token contract in Ethereum
"""
class ERC721Contract(BaseContract):
    
    """
    ERC721 Contract contstructor
    """
    def __init__(self, web3, address, abi=None, name=None, symbol=None, file_name=None):
        self.name = name
        self.symbol = symbol
        self.file_name = file_name
        if abi:
            super().__init__(web3, address, abi)
        else:
            fetched_abi = fetch_abi(erc721=True)
            if fetched_abi:
                super().__init__(web3, address, abi=fetched_abi)
            else:
                raise Exception("Could not fetch ABI for contract at address {}".format(address))
        
    def set_file_name(self):
        """
        Sets the file name for the output file
        """
        name = self.name if self.name is not None else self.address[2:12]
        self.file_name = "{}_erc721_transfers".format(name)
    
    def get_holders(self):
        """
        Get all holders of the contract
        This should always be called after the transactions are recorded
        """
        self.set_file_name()
        
        transactions = pd.read_csv("app/data/{}.csv".format(self.file_name))
        
        # sort by block_number ascending
        transactions = transactions.sort_values(by=['block_number'], ascending=True)
        
        # extract unique addresses from from and to columns and add them to the holders dataframe
        addresses = set(transactions['from'].values).union(set(transactions['to'].values))
        
        print("Found {} unique addresses".format(len(addresses)))
        
        # populate with 0 balance
        holders = {address: {'address': address, 'tokens': []} for address in addresses}
        
        holders = update_balances(holders, transactions, erc721=True)

        holders = pd.DataFrame(holders.values(), columns=['address', 'tokens'])
        
        holders.to_csv("app/data/{}_holders.csv".format(self.name), index=False)
    
    def record_transactions(self, from_block=0, to_block='latest'):
        """
        Fetches all transfers from the contract
        """
        web3_contract = self.to_token_contract()
        
        if to_block == 'latest':
            to_block = self.web3.eth.blockNumber
                
        self.set_file_name()
        
        # do the actual transaction recording
        do_record_transactions(
            self.address, 
            web3_contract, 
            self.file_name, 
            from_block, 
            to_block,
            erc721=True
        )
