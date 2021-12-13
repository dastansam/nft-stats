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
        return ERC20Contract(web3, TEST_CONTRACT, name="TEST")
    
    def get_default_abi(self):
        with open("app/abi/default-erc20.json") as f:
            return json.load(f)
    
    def test_initialize(self):
        contract = self.setup()
        self.assertEqual(contract.name, "TEST")
        self.assertEqual(contract.address, TEST_CONTRACT)
        self.assertEqual(contract.symbol, "None")
        
        default_abi = self.get_default_abi()
        self.assertEqual(contract.abi, default_abi)
        
    def test_set_file_name(self):
        contract = self.setup()
        contract.set_file_name()
        self.assertEqual(contract.file_name, '{}_erc20_transactions'.format("TEST"))
        
    def test_record_transactions(self):
        contract = self.setup()
        contract.record_transactions()
        
        # assert that file exists
        file_name = "{}_erc20_transactions.csv".format("TEST")
        self.assertTrue(os.path.isfile("app/data/{}".format(file_name)))
    
    def test_get_holders(self):
        contract = self.setup()
        
        self.assertRaisesRegex(
            Exception, 
            "Transactions are not recorded yet",
            contract.get_holders
        )
