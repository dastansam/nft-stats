import unittest
from app.utils import format_address, instantiate_web3
from app.config import INFURA_URL
from web3 import Web3

"""
Unit tests for utils.py
"""
class UtilsTest(unittest.TestCase):
    def test_web3_instantiation(self):
        invalid_url = 'https://invalid.url'
        self.assertRaises(ValueError, instantiate_web3, invalid_url)
        
        valid_url = INFURA_URL
        web3 = instantiate_web3(valid_url)
        self.assertIsInstance(web3, Web3)
        
    def test_format_address(self):
        address = '0x000000000000000000000000000000000000000011'
        formatted_address = format_address(address)
        self.assertEqual(formatted_address, '0x0000000000000000000000000000000000000000')
        invalid_address = '0x00000000000000000000000000000000000'
        self.assertRaises(IndexError, format_address, invalid_address)
