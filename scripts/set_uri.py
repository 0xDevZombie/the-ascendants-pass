#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    deployed_contract = TheAscendantsPass[len(TheAscendantsPass) - 1]
    deployed_contract.setTokenUri(1,
                                  "https://gateway.pinata.cloud/ipfs/QmT4qJK7gixgNL1SmKm4E51dery8PDdUxA3S1NppU1vR4M/1",
                                  {"from": dev})
    deployed_contract.setTokenUri(2,
                                  "https://gateway.pinata.cloud/ipfs/QmT4qJK7gixgNL1SmKm4E51dery8PDdUxA3S1NppU1vR4M/2",
                                  {"from": dev})
