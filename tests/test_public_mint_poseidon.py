import pytest
from brownie import TheAscendantsPass, network, accounts, reverts, web3
from .tokenID import Token_ID


# deployed contract with sale started
@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setTokenIdToMerkleRoot(Token_ID.GIFT_OF_POSEIDON.value,
                                      '0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 555)
    nft_contract.togglePublicSaleOpen(Token_ID.GIFT_OF_POSEIDON.value)
    return nft_contract


def test_can_mint_successfully(deployed_contract):
    deployed_contract.publicMint(Token_ID.GIFT_OF_POSEIDON.value, {"value": web3.toWei("0.2", "ether")})
    assert deployed_contract.balanceOf(accounts[0], Token_ID.GIFT_OF_POSEIDON.value) == 1
    assert deployed_contract.exists(2)


def test_cannot_mint_unknown_id(deployed_contract):
    with reverts("dev: tokenId unknown"):
        deployed_contract.publicMint(4)


def test_cannot_mint_twice(deployed_contract):
    deployed_contract.publicMint(Token_ID.GIFT_OF_POSEIDON.value, {"value": web3.toWei("0.2", "ether")})
    with reverts("dev: public allowance minted"):
        deployed_contract.publicMint(Token_ID.GIFT_OF_POSEIDON.value, {"value": web3.toWei("0.2", "ether")})


def test_cannot_mint_before_open_to_sale():
    nft_contract = TheAscendantsPass.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setMaxTokenSupply(Token_ID.GIFT_OF_POSEIDON.value, 55)
    with reverts("dev: public sale is not open"):
        nft_contract.publicMint(Token_ID.GIFT_OF_POSEIDON.value, {"value": web3.toWei("0.2", "ether")})


def test_cannot_mint_below_mint_price(deployed_contract):
    with reverts("dev: msg.value too low"):
        deployed_contract.publicMint(Token_ID.GIFT_OF_POSEIDON.value, {"value": web3.toWei("0.15", "ether")})

# def test_cannot_mint_more_then_cap_goz(deployed_contract):
#     for x in range(888):
#         new_acc = accounts.add()
#         accounts[1].transfer(new_acc, web3.toWei(0.2, "ether"))
#         deployed_contract.addToWhiteList([new_acc], {"from": accounts[0]})
#         deployed_contract.safeMint(new_acc, {"from": new_acc, "value": web3.toWei(0.1, "ether")})
#     with reverts("dev: max token supply minted"):
#         deployed_contract.safeMint(accounts[0], {"value": web3.toWei(0.1, "ether")})
