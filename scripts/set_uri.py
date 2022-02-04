#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    deployed_contract = TheAscendantsPass[len(TheAscendantsPass) - 1]
    deployed_contract.setTokenIdToUri(1,
                                  "ipfs://Qmc3K7mEsDmEYRewB19hzszDdPm4wkVmBo53oRFtk1114B/",
                                  {"from": dev})
    # deployed_contract.setTokenIdToUri(2,
    #                               "ipfs://QmfFRSopoyvexDCf9L5dEAoELXCqUVUsNHWRkgJqsyCv3p/gop",
    #                               {"from": dev})


# ipfs://Qmd6dZyHyzjG7XBT8uFC6nMuB3S9jq9ht9Wi4zNQgzFGDY/