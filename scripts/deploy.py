#!/usr/bin/python3
import os
from brownie import TheAscendantsPass, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    TheAscendantsPass.deploy("0xFE34d6B98630f4deb6064b9D46B7F3861675c8DB", {"from": dev}, publish_source=False)

