import pytest
from brownie import TheAscendantsPass, network, accounts, reverts, web3
from enum import Enum


@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = TheAscendantsPass.deploy(accounts[0],{"from": accounts[0]})
    return nft_contract


def test_deployer_is_owner(deployed_contract):
    assert deployed_contract.owner() == accounts[0]


def test_can_transfer_ownership(deployed_contract):
    deployed_contract.transferOwnership(accounts[1] ,{"from": accounts[0]})
    assert deployed_contract.owner() == accounts[1]


def test_non_owner_cannot_transfer_ownership(deployed_contract):
    with reverts("Ownable: caller is not the owner"):
        deployed_contract.transferOwnership(accounts[1], {"from": accounts[1]})
