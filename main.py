"""
Main executable file of the project.
The workflow is as follows:
- Gets the arguments from the command line
- Instantiates the web3 object with the Infura URL
- Based on the arguments, either:
    - Gets the ERC20 contract
        - If input file is not flagged:
            - Extracts transactions from the blockchain
        - Extracts holders from the contract
    - Gets the ERC721 contract
        - If input file is not flagged:
            - Extracts transactions from the blockchain
        - Extracts holders from the contract
"""

from app.classes.erc721 import ERC721Contract
from app.utils import instantiate_web3
from app.config import INFURA_URL
from app.classes.erc20 import ERC20Contract
from app.parser import parser

CONTRACT_ADDRESS = "0x1CB1A5e65610AEFF2551A50f76a87a7d3fB649C6"

print("Launching app ...")

def main():
    print("Instantiating contract...")
    web3 = instantiate_web3(INFURA_URL)
    
    (options, args) = parser.parse_args()
    
    if not options.address:
        print("Using test contract address: {}".format(CONTRACT_ADDRESS))
    
        checksum_address = web3.toChecksumAddress(CONTRACT_ADDRESS)
    else:
        print("Using contract address: {}".format(options.address))
        checksum_address = web3.toChecksumAddress(options.address)
    
    # block number to start extracting events from
    block_range = int(options.blockrange) if options.blockrange else 1000
    from_block = web3.eth.block_number - block_range
    
    print("Block range: {}".format(block_range))
    
    if options.erc721:
        nft = ERC721Contract(
            web3,
            checksum_address, 
            name=options.name,
            symbol=options.symbol,
        )
        if options.infile:
            print("Reading from file: {}".format(options.infile))
            nft.get_holders(input=options.infile)
            print("Done!")
            return
        
        nft.record_transactions(from_block=from_block, block_range=block_range, output=options.outfile)
        print("Recorded transactions from block: {}".format(from_block))

        nft.get_holders()
        print("Done!")
        return

    # contract = ERC20Contract(web3, checksum_address, name="anyswap", symbol="celo")
    print("Getting logs ...")
    
    erc20 = ERC20Contract(web3, checksum_address, name=options.name, symbol=options.symbol)

    if options.infile:
        print("Reading from file: {}".format(options.infile))
        erc20.get_holders(input=options.infile)
        print("Done!")
        return
    
    erc20.record_transactions(from_block=from_block, block_range=block_range, output=options.outfile)
    print("Fetched transactions from block: {}".format(from_block))
    
    erc20.get_holders()
    print("Done!")
    return


# run the main function
if __name__ == "__main__":
    main()
