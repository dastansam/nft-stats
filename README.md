# Extracting ERC20 and ERC721 Token holders

## Abstract

ERC20 is an Ethereum spec for fungible tokens, while ERC721 is for non-fungible tokens (aka NFTs). Since tokens transfers are not registered on blockchain as native transfer transaction, it's often very hard to query data specific to abovementioned tokens. For example, if you want to retrieve all token holders of some specific ERC20 token, you can not directly query it from blockchain. Although smart contracts store the mapping of token holders to their balances, it's not exposed to outside. Etherscan displays data about holders and events, but it's not complete and it's API doesn't have endpoints where you can query the data you need. Therefore, we should look for alternative solutions.

## Solution

Although, ERC20 token transfers are not registered as a transaction, every token transfer emits a Transfer event. Ethereum stores every emitted event (aka log) in the block data. Therefore, if we have the token address and ABI, we could theoretically query the blockchain for Events emitted from the token address and form a database of transfers and holders.

## Implementation

We should essentially query the needed events for us via `eth_getLogs` call. This will return logs that were emitted filered by provided parameters. For example, we will need to provide block ranges (from_block, to_block) and event Topic (essentially, hash of the Event type), contract address, etc.

There is one well-known limitation of `eth_getLogs`: the query usually fails with timeout if there are more than 1000 logs returned in one query. To tackle this issue, I used very naive approach: every query is only for 1000 block range. This is to ensure that we don't hit the timeout error. More sophisticated strategy could have been designed, but this is the approach that meets the time and resource requirements.

While loop will decrement the `to_block` and `from_block` arguments by 1000 in each iteration and will break if the from_block is less than or equal to 0 (i.e genesis block), or if the query returns 0 logs.

## Notes

Since the blockchain state is not constant, it's hard to test our script. There are always transfers and exchanges happening on Ethereum chain. So, the data now, may become obsolete the next second.

To eye test the results, you can use Etherscan. For example, in the file that contains the holders of a certain ERC721 token, copy the holder address and insert in Etherscan. And in the portfolio of the user, select that certain ERC721 token. And in the `inventory` tab below, you will see the list of `token_ids`. Check if the list that we have is similar to that on Etherscan.

## Contents

- `main.py`   
    In the parent directory, there is a `main.py` file, which is an executable file of the project. It parses provided command line arguments and launches the token holders extraction function.

- `app`  
    This folder contains the business logic of the project.

    - `abi`
      - This folder contains the default `ABI`s for both ERC20 and ERC721 token smart contracts
      - It is used as a fallback ABI when we can't fetch the ABI of contract from Etherscan
    - `data`
      - This folder is an empty folder initially. Will be populated by csv files that are generated as a result of our query
    - `config.py`
      - Contains environmental variables and constants specific to the project
    - `ethereum.py`
      - Contains functions that are used for interacting with Ethereum chain
    - `utils.py`
      - Contains utility functions used across the project
    - `parser.py`
      - Contains command line argument parser configuration
    - `classes`
      - Contains classes that represent types of tokens
      - `base_contract.py`
        - Abstract class that represents an Ethereum contract
      - `ERC20Contract.py`
        - Class that represents smart contract of an `ERC20` token
      - `ERC721Contract.py`
        - Class that represents smart contract of an `ERC721` token

