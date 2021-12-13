"""
Class that represents an ERC20 token contract in Ethereum
"""

from app.utils import fetch_abi
from app.ethereum import do_record_transactions, update_balances
from app.classes.base_contract import BaseContract
import csv


class ERC20Contract(BaseContract):
    
    """
    ERC20 Contract contstructor
    :param web3: Web3 instance
    :type web3: Web3
    :param address: Address of the contract
    :param abi: ABI of the contract
    :type abi: list
    :param name: Name of the contract
    :type name: str
    :param symbol: Symbol of the contract
    :type symbol: str
    :param file_name: Name of the file to save the transactions to
    :type file_name: str
    """
    def __init__(self, web3, address, abi=None, name=None, symbol=None, file_name=None):
        self.name = name
        self.symbol = symbol
        self.file_name = file_name
        
        if abi:
            super().__init__(web3, address, abi)
        else:
            fetched_abi = fetch_abi()
            super().__init__(web3, address, abi=fetched_abi)
    
    def set_file_name(self):
        """
        Setter for the file name
        """
        name = self.name if self.name is not None else self.address[2:12]
        self.file_name = '{}_erc20_transactions'.format(name)
        
    def get_holders(self, input=None, output=None):
        """
        Get all holders of the contract
        This should always be called after the transactions are recorded
        :param input: Input file
        :type input: str
        :param output: Output file
        :type output: str
        """
        self.set_file_name()
        
        input_path = input if input else "app/data/{}.csv".format(self.file_name)
        
        with open(input_path, "r") as transactions:
            transactions = csv.reader(transactions)

            # sort by block_number ascending
            sorted_transactions = sorted(transactions, key=lambda k: k[3])
            
            print("Total number of transactions: {}".format(len(sorted_transactions)))
    
            # get all unique holders
            addresses = set()
            for transaction in sorted_transactions:
                # skip header row
                if transaction[1] == 'to':
                    pass
                addresses.add(transaction[0])
                addresses.add(transaction[1])
            
            print("Found {} unique addresses".format(len(addresses)))
            
            # populate with 0 balance
            holders = {address: {'address': address, 'balance': 0} for address in addresses}
            
            print("Updating balances...")
            # do actually update the balances
            holders = update_balances(holders, sorted_transactions)

            print("Updated balances")
            
            output_path = output if output else "app/data/{}_holders.csv".format(self.file_name)

            writer = csv.DictWriter(
                open(output_path, "w"),
                fieldnames=['address', 'balance']
            )
            writer.writeheader()
            writer.writerows(holders.values())

    def record_transactions(self, from_block=0, to_block='latest', block_range=1000, output=None):
        """
        Fetch all Transfer events in the blockchain
        and save them to the csv file
        :param from_block: Starting block
        :type from_block: int
        :param to_block: Ending block
        :type to_block: int
        :param block_range: Number of blocks to fetch in one go
        :type block_range: int
        :param output: Output file
        :type output: str
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
            block_range=block_range,
            initial_to_block=to_block,
            output=output
        )
     
    def __str__(self):
        return "ERC20 Contract: {}".format(self.address)
