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
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_POSEIDON.value,
                                        '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    return nft_contract


def test_cannot_toggle_public_sale_of_goz(deployed_contract):
    with reverts("dev: public mint not allowed for this token"):
        deployed_contract.togglePublicSaleOpen(Token_ID.GIFT_OF_ZEUS.value)


def test_set_mint_price(deployed_contract):
    deployed_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 555)
    deployed_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_POSEIDON.value)
    deployed_contract.setTokenIdToMintPrice(Token_ID.GIFT_OF_POSEIDON.value, web3.toWei("0.4", "ether"))
    with reverts("dev: msg.value too low"):
        deployed_contract.privateMint(Token_ID.GIFT_OF_POSEIDON.value, accounts_merkle_proof[0],
                                      {"value": web3.toWei("0.2", "ether")})
    deployed_contract.privateMint(Token_ID.GIFT_OF_POSEIDON.value, accounts_merkle_proof[0],
                                  {"value": web3.toWei("0.4", "ether")})
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_POSEIDON.value) == 1
    assert deployed_contract.exists(2)


def test_cannot_set_mint_price_for_goz(deployed_contract):
    with reverts("dev: cannot set price for this token"):
        deployed_contract.setTokenIdToMintPrice(Token_ID.GIFT_OF_ZEUS.value, web3.toWei("0.4", "ether"))


def test_can_set_uri(deployed_contract):
    some_uri = "http.website.com"
    deployed_contract.setTokenIdToUri(Token_ID.GIFT_OF_ZEUS.value, some_uri)
    assert deployed_contract.uri(Token_ID.GIFT_OF_ZEUS.value) == some_uri
