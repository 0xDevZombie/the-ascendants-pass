#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    deployed_contract = TheAscendantsPass[len(TheAscendantsPass) - 1]
    # deployed_contract.setTokenIdToUri(1,
    #                               "ipfs://Qma4mpRR9BTWTJxCwy1WxDMwXvYCDibomuUcRDpePDT17Q/1",
    #                               {"from": dev})
    deployed_contract.setTokenIdToUri(2,
                                  "ipfs://Qma4mpRR9BTWTJxCwy1WxDMwXvYCDibomuUcRDpePDT17Q/2",
                                  {"from": dev})


# ipfs://Qmd6dZyHyzjG7XBT8uFC6nMuB3S9jq9ht9Wi4zNQgzFGDY/