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
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 55)
    nft_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_ZEUS.value)
    return nft_contract


def test_can_mint_successfully(deployed_contract):
    deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_ZEUS.value) == 1
    assert deployed_contract.exists(1)

def test_cannot_mint_unknown_id(deployed_contract):
    with reverts("dev: tokenId unknown"):
        deployed_contract.privateMint(4, accounts_merkle_proof[0])

def test_cannot_mint_twice(deployed_contract):
    deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])
    with reverts("dev: whitelist allowance minted"):
        deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])

def test_cannot_mint_before_open_to_sale():
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 55)
    with reverts("dev: sale is not open currently"):
        nft_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])



def test_cannot_mint_more_then_cap_goz():
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_ZEUS.value,
                                        '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 2)
    nft_contract.togglePrivateSaleOpen(Token_ID.GIFT_OF_ZEUS.value)
    nft_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0],
                                  {"value": web3.toWei("0.2", "ether")})
    nft_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[1],
                                  {"from": accounts[1], "value": web3.toWei("0.2", "ether")})

    with reverts("dev: max token supply minted"):
        nft_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[2],
                                      {"from": accounts[2], "value": web3.toWei("0.2", "ether")})

def test_cannot_mint_if_sale_is_not_open():
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_ZEUS.value,
                                        '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_ZEUS.value, 555)
    with reverts("dev: sale is not open currently"):
        nft_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0])

def test_cannot_if_not_on_whitelist_no_proof(deployed_contract):
    with reverts("dev: not on the whitelist"):
        deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, [], {"from": accounts[9]})

def test_cannot_if_not_on_whitelist_wrong_proof_but_on_wl(deployed_contract):
    with reverts("dev: not on the whitelist"):
        deployed_contract.privateMint(Token_ID.GIFT_OF_ZEUS.value, accounts_merkle_proof[0], {"from": accounts[1]})
