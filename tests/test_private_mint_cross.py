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
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_POSEIDON.value,
                                        '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 55)
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 55)
    nft_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_ZEUS.value)
    nft_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_POSEIDON.value)
    return nft_contract


def test_cannot_mint_twice(deployed_contract):
    deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])
    with reverts("dev: whitelist allowance minted"):
        deployed_contract.privateMint(Token_ID.GIFT_OF_POSEIDON.value, accounts_merkle_proof[0], {"value": web3.toWei("0.2", "ether")})
