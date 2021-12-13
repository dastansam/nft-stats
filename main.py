from app.classes.erc721 import ERC721Contract
from app.utils import instantiate_web3
from app.config import INFURA_URL
from app.classes.erc20 import ERC20Contract

CONTRACT_ADDRESS = "0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6"
print("Launching app ...")
def main():
    web3 = instantiate_web3(INFURA_URL)
    print("Instantiating contract...")
    
    checksum_address = web3.toChecksumAddress(CONTRACT_ADDRESS)
    # contract = ERC20Contract(web3, checksum_address, name="anyswap", symbol="celo")
    print("Getting logs ...")
    
    nft = ERC721Contract(web3, checksum_address, name="TOADZ", symbol="TOADZ")
    
    from_block = web3.eth.block_number - 1000
    print("From block: {}".format(from_block))
    # contract.fetch_transactions(from_block)
    
    print('Extracting holders...')
    
    # nft.record_transactions(from_block)
    nft.get_holders()


# run the main function
if __name__ == "__main__":
    main()
