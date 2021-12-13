# Instructions

## Install

First, clone this repository:

```
git clone https://github.com/dastansam/nft-stats.git
```

Go to the folder `nft-stats`:

```
cd nft-stats
```

Initialize virtual environment:

```
virtualenv venv
```

Install packages:

```
pip install -r requirements.txt
```

## Run

To run the package, execute the `main.py` file by providing arguments.
```
python main.py [options]
```
To easily test the script, you can get the values for arguments from `test-contracts.json` file.

For example, for `TetherGold` ERC20 token:

```
python main.py -a "0x68749665ff8d2d112fa859aa293f07a622782f38" -n "TetherGold" -s "Tgld" -r 50000
```

These are the breakdown of arguments:

```
-a, --address: Contract address, required
-n, --name: Name of the token
-s, --symbol: Symbol of the token
-r, --blockrange: Block ranges to use for querying Transfer events from Ethereum chain
-i, --infile: A boolean flag that indicates whether transactions csv file is already populated
-o, --outfile: Output file
-c, --erc721: A boolean flag that indicates whether contract is an ERC721 token
```

For tokens where there are many activities happening on chain, i.e many Transfer events in the block range, it's advised to supply fewer block range. For example, 1000 block range is pretty good range for most of the tokens.

And for tokens with less activities, you can supply the bigger block range. For example, 50000 blocks.

Finally, just watch how script performs, if it fails with `more than 10000 events returned in query`, you should decrease the block range.

## Tests

To perform the tests:
```

```
