"""
A base abstract class that represents a Contract in Ethereum
Has ABI and address
This class is used to extract useful information from the contract
"""
class BaseContract:
    
    """
    Contract contstructor
    """
    def __init__(self, web3, address, abi):
        self.web3 = web3     
        self.address = address
        self.abi = abi

    def to_token_contract(self):
        """
        Converts the contract to a web3 contract instance
        """
        contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        return contract
