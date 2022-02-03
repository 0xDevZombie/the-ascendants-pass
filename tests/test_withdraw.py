import pytest
from brownie import TheAscendantsPass, network, accounts, reverts, web3
from enum import Enum
from .merkle_proofs import accounts_merkle_proof
from .tokenID import Token_ID

@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = TheAscendantsPass.deploy(accounts[0],{"from": accounts[0]})
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_POSEIDON.value,
                                        '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 555)
    nft_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_POSEIDON.value)
    return nft_contract



def test_withdraw(deployed_contract):
    for x in range(5):
        deployed_contract.privateMint(Token_ID.GIFT_OF_POSEIDON.value, accounts_merkle_proof[x],
                                      {"from": accounts[x], "value": web3.toWei("0.2", "ether")})

    pre_balance = web3.fromWei(accounts[0].balance(), "ether")
    deployed_contract.withdrawFunds()
    after_balance = web3.fromWei(accounts[0].balance(), "ether")
    assert after_balance - pre_balance == 1

def test_only_owner_can_withdraw(deployed_contract):
    with reverts("Ownable: caller is not the owner"):
        deployed_contract.withdrawFunds({"from": accounts[1]})

