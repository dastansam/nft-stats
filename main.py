from app.utils import instantiate_web3
from app.config import INFURA_URL
from app.classes.contract import ERC20Contract

COMPOUND_ADDRESS = "0xc00e94cb662c3520282e6f5717214004a7f26888"
print("Launching app ...")
def main():
    web3 = instantiate_web3(INFURA_URL)
    print("Instantiating contract...")
    checksum_address = web3.toChecksumAddress(COMPOUND_ADDRESS)
    contract = ERC20Contract(web3, checksum_address, name="Comp", symbol="comp")
    print("Getting logs ...")
    
    from_block = web3.eth.block_number - 1000
    print("From block: {}".format(from_block))
    contract.fetch_transactions(from_block)


# run the main function
if __name__ == "__main__":
    main()
