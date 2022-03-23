#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    deployed_contract = TheAscendantsPass[len(TheAscendantsPass) - 1]
    # deployed_contract.setTokenIdToMerkleRoot(1, "0x922a4c61218604bea044b635d2d87a6c379a6f3886a173fca8e959dae35cffc4", {"from": dev})
    deployed_contract.setTokenIdToMerkleRoot(2, "0xd835fcdfa6cb64a3e50a7bbff689011d3468fee6da184a396652cfcf9b5824c4", {"from": dev})

