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
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_POSEIDON.value,
                                      '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 1)
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 555)
    nft_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_POSEIDON.value)
    nft_contract.curatorAward(Token_ID.GIFT_OF_POSEIDON.value)
    return nft_contract


def test_can_burn_mint(deployed_contract):
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_POSEIDON.value) == 40
    assert deployed_contract.exists(2)
    deployed_contract.toggleBurnMint()
    deployed_contract.burnMint()
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_POSEIDON.value) == 36
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_ZEUS.value) == 1
    assert deployed_contract.exists(1)

def test_cannot_call_without_4_tokens(deployed_contract):
    deployed_contract.toggleBurnMint()
    with reverts("dev: not enough tokens"):
        deployed_contract.burnMint({"from": accounts[1]})

def test_cannot_cannot_call_when_not_enabled(deployed_contract):
    with reverts("dev: burn mint not enabled"):
        deployed_contract.burnMint({"from": accounts[1]})




