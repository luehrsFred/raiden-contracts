import pytest
from eth_tester.exceptions import TransactionFailed


def test_token_mint(web3, custom_token, get_accounts):
    (A, B) = get_accounts(2)
    token = custom_token
    multiplier = custom_token.functions.multiplier().call()
    supply = token.functions.totalSupply().call()

    token_pre_balance = web3.eth.getBalance(token.address)
    tokens = 50 * multiplier
    token.functions.mint(tokens).transact({'from': A})
    assert token.functions.balanceOf(A).call() == tokens
    assert token.functions.totalSupply().call() == supply + tokens
    assert web3.eth.getBalance(token.address) == token_pre_balance


def test_approve_transfer(web3, custom_token, get_accounts):
    (A, B) = get_accounts(2)
    token = custom_token
    token.functions.mint(50).transact({'from': A})
    initial_balance_A = token.functions.balanceOf(A).call()
    initial_balance_B = token.functions.balanceOf(B).call()
    to_transfer = 20
    token.functions.approve(B, to_transfer).transact({'from': A})
    token.functions.transferFrom(A, B, to_transfer).transact({'from': B})
    assert token.functions.balanceOf(B).call() == initial_balance_B + to_transfer
    assert token.functions.balanceOf(A).call() == initial_balance_A - to_transfer


def test_token_transfer_funds(web3, custom_token, get_accounts, txn_gas):
    (A, B) = get_accounts(2)
    token = custom_token
    multiplier = custom_token.functions.multiplier().call()
    assert multiplier > 0
    supply = token.functions.totalSupply().call()
    assert supply > 0

    owner = custom_token.functions.owner_address().call()

    with pytest.raises(TransactionFailed):
        token.functions.transferFunds().transact({'from': owner})

    token.functions.mint(50).transact({'from': A})
    assert web3.eth.getBalance(token.address) == 0
