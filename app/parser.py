"""
Contains command line argument parser for the application.
"""

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-a", "--address", dest="address",
                  help="Contract address", metavar="ADDRESS")

parser.add_option("-n", "--name", dest="name",
                  help="Contract name", metavar="NAME")

parser.add_option("-s", "--symbol", dest="symbol",
                  help="Contract symbol", metavar="SYMBOL")

parser.add_option("-c", "--erc721", dest="erc721",
                  help="Contract is ERC721", metavar="ERC721")

parser.add_option("-i", "--infile", dest="infile",
                  help="Input file", metavar="INFILE")

parser.add_option("-o", "--outfile", dest="outfile",
                  help="Output file", metavar="OUTFILE")

parser.add_option("-r", "--blockrange", dest="blockrange",
                  help="Block range", metavar="BLOCKRANGE")
