import unittest
from app.classes.erc20 import ERC20Contract
from app.config import INFURA_URL
from app.utils import instantiate_web3
import json
import os

TEST_CONTRACT = "0x68749665ff8d2d112fa859aa293f07a622782f38"

class ERC20Test(unittest.TestCase):
    def setup(self):
        web3 = instantiate_web3(INFURA_URL)
        checksum_address = web3.toChecksumAddress(TEST_CONTRACT)
        return ERC20Contract(web3, checksum_address, name="TEST")
    
    def get_default_abi(self):
        with open("app/abi/default-erc20.json") as f:
            return json.load(f)
    
    def test_initialize(self):
        contract = self.setup()
        checksum_address = contract.web3.toChecksumAddress(TEST_CONTRACT)
        
        self.assertEqual(contract.name, "TEST")
        self.assertEqual(contract.address, checksum_address)
        self.assertEqual(contract.symbol, None)
        
        default_abi = self.get_default_abi()
        self.assertEqual(contract.abi, default_abi)
        
    def test_set_file_name(self):
        contract = self.setup()
        contract.set_file_name()
        self.assertEqual(contract.file_name, '{}_erc20_transactions'.format("TEST"))
        
    def test_record_transactions(self):
        contract = self.setup()
        from_block = contract.web3.eth.block_number
        
        contract.record_transactions(
            from_block=from_block - 1000,
            to_block=contract.web3.eth.block_number,
            block_range=1000,
            output="test/expected-data/TEST_erc_20_transfers_generated.csv"
        )
        
        # assert that file exists
        self.assertTrue(os.path.isfile("test/expected-data/TEST_erc_20_transfers_generated.csv"))
    
    def test_get_holders(self):
        contract = self.setup()
        
        contract.get_holders(
            input="test/test-data/TEST_erc_20_transfers.csv",
            output="test/expected-data/TEST_erc_20_holders_generated.csv"
        )

        self.assertTrue(os.path.isfile("test/expected-data/TEST_erc_20_holders_generated.csv"))


if __name__ == '__main__':
    unittest.main()
