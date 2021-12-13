import unittest

from app.utils import format_address, instantiate_web3
from app.config import INFURA_URL
from web3 import Web3
from eth_utils.hexadecimal import decode_hex

"""
Unit tests for utils.py
"""
class UtilsTest(unittest.TestCase):
    def test_web3_instantiation(self):
        invalid_url = 'https://invalid.url'
        invalid_instance = instantiate_web3(invalid_url)
        self.assertFalse(invalid_instance.provider.isConnected())
        
        valid_url = INFURA_URL
        web3 = instantiate_web3(valid_url)
        self.assertIsInstance(web3, Web3)
        
    def test_format_address(self):
        address = decode_hex('0x000000000000000000000000000000000000000011')
        formatted_address = format_address(address)
        self.assertEqual(formatted_address, '0x0000000000000000000000000000000000000011')
        
        unchanged_address = decode_hex('0x0000000000000000000000000000000000000011')
        
        self.assertEqual(format_address(unchanged_address), "0x0000000000000000000000000000000000000011")


if __name__ == '__main__':
    unittest.main()
