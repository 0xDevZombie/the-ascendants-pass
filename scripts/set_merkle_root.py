#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    deployed_contract = TheAscendantsPass[len(TheAscendantsPass) - 1]
    deployed_contract.setTokenIdToMerkleRoot(1, "0x6d2236811f8af82a90939617e52217847b079ed0099b01e3f976849fc72d93b4", {"from": dev})
    deployed_contract.setTokenIdToMerkleRoot(2, "0x6d2236811f8af82a90939617e52217847b079ed0099b01e3f976849fc72d93b4", {"from": dev})

