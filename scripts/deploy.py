#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    TheAscendantsPass.deploy("0xc5A5950f11A096dfAb41c2ee387D5e998c7b8de0", {"from": dev}, publish_source=True)

