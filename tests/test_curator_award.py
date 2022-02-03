import pytest
from brownie import TheAscendantsPass, network, accounts, reverts, web3
from .tokenID import Token_ID

account_0_merkle_proof = ['0xb71ab4ebd064346093c6ea89e4080ee03ad86b6e2abfa76a22bcbf905469d0e7',
                          '0x0454fd97f70467612e870296d46e6a9ffcab6655b800a6ee4713273c687025a2',
                          '0x344d536da52f2f25e5f9e89b357952f4ed7fdf6a74025f4a9098dc355396695a']


# deployed contract with sale started
@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    return nft_contract


def test_can_call_curator_award(deployed_contract):
    deployed_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 55)
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_POSEIDON.value) == 0
    deployed_contract.curatorAward(Token_ID.GIFT_OF_POSEIDON.value)
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_POSEIDON.value) == 40
    assert deployed_contract.exists(2)


def test_cannot_call_curator_award_twice(deployed_contract):
    deployed_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 100)
    deployed_contract.curatorAward(Token_ID.GIFT_OF_POSEIDON.value)
    with reverts("dev: cannot claim curator award again"):
        deployed_contract.curatorAward(Token_ID.GIFT_OF_POSEIDON.value)

def test_cannot_call_curator_award_for_goz(deployed_contract):
    deployed_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 55)
    with reverts("dev: curator award not allowed for this tokenId"):
        deployed_contract.curatorAward(Token_ID.GIFT_OF_ZEUS.value)

def test_cannot_breach_max_token_supply(deployed_contract):
    with reverts("dev: max token supply minted"):
        deployed_contract.curatorAward(Token_ID.GIFT_OF_POSEIDON.value)




