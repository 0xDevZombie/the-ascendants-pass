import pytest
from brownie import TheAscendantsPass, network, accounts, reverts, web3
from .tokenID import Token_ID
from .merkle_proofs import accounts_merkle_proof


# deployed contract with sale started
@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_ZEUS.value,
                                        '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')

    return nft_contract


def test_can_view_remaining_mints_goz(deployed_contract):
    deployed_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 10)
    deployed_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_ZEUS.value)
    deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])
    assert deployed_contract.getTokenIdToRemainingMints(Token_ID.GIFT_OF_ZEUS.value) == 9
    deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[1],
                                  {"from": accounts[1]})
    assert deployed_contract.getTokenIdToRemainingMints(Token_ID.GIFT_OF_ZEUS.value) == 8


def test_can_view_remaining_mints_gop(deployed_contract):
    deployed_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_POSEIDON.value,
                                             '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    deployed_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 100)
    deployed_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_POSEIDON.value)
    deployed_contract.privateMint(Token_ID.GIFT_OF_POSEIDON.value, accounts_merkle_proof[0],
                                  {"from": accounts[0], "value": web3.toWei("0.2", "ether")})
    assert deployed_contract.getTokenIdToRemainingMints(Token_ID.GIFT_OF_POSEIDON.value) == 99
    deployed_contract.privateMint(Token_ID.GIFT_OF_POSEIDON.value, accounts_merkle_proof[1],
                                  {"from": accounts[1], "value": web3.toWei("0.2", "ether")})
    assert deployed_contract.getTokenIdToRemainingMints(Token_ID.GIFT_OF_POSEIDON.value) == 98
