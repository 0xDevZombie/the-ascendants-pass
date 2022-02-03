#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    deployed_contract = TheAscendantsPass[len(TheAscendantsPass) - 1]
    deployed_contract.setTokenIdToMerkleRoot(1, "0x120fe8aa6205c212329642fab0471e6cae952b7672d54ee6cd810499b8b5e9dc", {"from": dev})

