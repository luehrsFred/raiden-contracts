import pytest
from ethereum import tester
from raiden_contracts.utils.events import check_channel_settled
from .fixtures.config import empty_address
from raiden_contracts.utils.config import E_CHANNEL_SETTLED


def test_cooperative_settle_channel_call(
        token_network,
        create_channel_and_deposit,
        get_accounts,
        create_cooperative_settle_signatures,
        cooperative_settle_state_tests
):
    (A, B, C) = get_accounts(3)
    deposit_A = 20
    deposit_B = 10
    balance_A = 5
    balance_B = 25

    channel_identifier = create_channel_and_deposit(A, B, deposit_A, deposit_B)

    (signature_A, signature_B) = create_cooperative_settle_signatures(
        [A, B],
        channel_identifier,
        A, balance_A,
        B, balance_B
    )

    with pytest.raises(TypeError):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, -1,
            B, balance_B,
            signature_A,
            signature_B
        )
    with pytest.raises(TypeError):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            B, -1,
            signature_A,
            signature_B
        )
    with pytest.raises(TypeError):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            0x0, balance_A,
            B, balance_B,
            signature_A,
            signature_B
        )
    with pytest.raises(TypeError):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            0x0, balance_B,
            signature_A,
            signature_B
        )
    with pytest.raises(TypeError):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            B, balance_B,
            0x0,
            signature_B
        )
    with pytest.raises(TypeError):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            B, balance_B,
            signature_A,
            0x0
        )

    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            empty_address,
            balance_A,
            B, balance_B,
            signature_A,
            signature_B
        )
    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            empty_address,
            balance_B,
            signature_A,
            signature_B
        )

    token_network.transact({'from': C}).cooperativeSettle(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        signature_A,
        signature_B
    )


def test_cooperative_settle_channel_signatures(
        token_network,
        create_channel_and_deposit,
        get_accounts,
        create_cooperative_settle_signatures
):
    (A, B, C) = get_accounts(3)
    deposit_A = 20
    deposit_B = 10
    balance_A = 4
    balance_B = 26

    channel_identifier = create_channel_and_deposit(A, B, deposit_A, deposit_B)

    (signature_A, signature_B, signature_C) = create_cooperative_settle_signatures(
        [A, B, C],
        channel_identifier,
        A, balance_A,
        B, balance_B
    )

    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            B, balance_B,
            signature_C,
            signature_B
        )
    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A,
            B, balance_B,
            signature_A,
            signature_C
        )
    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_B,
            B, balance_A,
            signature_A,
            signature_B
        )

    token_network.transact({'from': C}).cooperativeSettle(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        signature_A,
        signature_B
    )


def test_cooperative_settle_channel_0(
        custom_token,
        token_network,
        create_channel_and_deposit,
        get_accounts,
        create_cooperative_settle_signatures,
        cooperative_settle_state_tests
):
    (A, B, C) = get_accounts(3)
    deposit_A = 20
    deposit_B = 10
    balance_A = 0
    balance_B = 30

    channel_identifier = create_channel_and_deposit(A, B, deposit_A, deposit_B)

    (signature_A, signature_B, signature_C) = create_cooperative_settle_signatures(
        [A, B, C],
        channel_identifier,
        A, balance_A,
        B, balance_B
    )

    pre_account_balance_A = custom_token.call().balanceOf(A)
    pre_account_balance_B = custom_token.call().balanceOf(B)
    pre_balance_contract = custom_token.call().balanceOf(token_network.address)

    token_network.transact({'from': C}).cooperativeSettle(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        signature_A,
        signature_B
    )

    cooperative_settle_state_tests(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        pre_account_balance_A,
        pre_account_balance_B,
        pre_balance_contract
    )


def test_cooperative_settle_channel_00(
        custom_token,
        token_network,
        create_channel_and_deposit,
        get_accounts,
        create_cooperative_settle_signatures,
        cooperative_settle_state_tests
):
    (A, B, C) = get_accounts(3)
    deposit_A = 0
    deposit_B = 0
    balance_A = 0
    balance_B = 0

    channel_identifier = create_channel_and_deposit(A, B, deposit_A, deposit_B)

    (signature_A, signature_B, signature_C) = create_cooperative_settle_signatures(
        [A, B, C],
        channel_identifier,
        A, balance_A,
        B, balance_B
    )

    pre_account_balance_A = custom_token.call().balanceOf(A)
    pre_account_balance_B = custom_token.call().balanceOf(B)
    pre_balance_contract = custom_token.call().balanceOf(token_network.address)

    token_network.transact({'from': C}).cooperativeSettle(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        signature_A,
        signature_B
    )

    cooperative_settle_state_tests(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        pre_account_balance_A,
        pre_account_balance_B,
        pre_balance_contract
    )


def test_cooperative_settle_channel_state(
        web3,
        custom_token,
        token_network,
        create_channel_and_deposit,
        get_accounts,
        create_cooperative_settle_signatures,
        cooperative_settle_state_tests
):
    (A, B, C) = get_accounts(3)
    deposit_A = 20
    deposit_B = 10
    balance_A = 5
    balance_B = 25

    channel_identifier = create_channel_and_deposit(A, B, deposit_A, deposit_B)

    (signature_A, signature_B) = create_cooperative_settle_signatures(
        [A, B],
        channel_identifier,
        A, balance_A,
        B, balance_B
    )

    pre_account_balance_A = custom_token.call().balanceOf(A)
    pre_account_balance_B = custom_token.call().balanceOf(B)
    pre_balance_contract = custom_token.call().balanceOf(token_network.address)

    token_network.transact({'from': C}).cooperativeSettle(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        signature_A,
        signature_B
    )

    cooperative_settle_state_tests(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        pre_account_balance_A,
        pre_account_balance_B,
        pre_balance_contract
    )


def test_cooperative_settle_channel_wrong_balances(
        web3,
        custom_token,
        token_network,
        create_channel_and_deposit,
        get_accounts,
        create_cooperative_settle_signatures,
        cooperative_settle_state_tests
):
    (A, B, C) = get_accounts(3)
    deposit_A = 20
    deposit_B = 10
    balance_A = 7
    balance_B = 23

    balance_A_fail1 = 20
    balance_B_fail1 = 11
    balance_A_fail2 = 6
    balance_B_fail2 = 8

    channel_identifier = create_channel_and_deposit(A, B, deposit_A, deposit_B)

    (signature_A, signature_B) = create_cooperative_settle_signatures(
        [A, B],
        channel_identifier,
        A, balance_A,
        B, balance_B
    )
    (signature_A_fail1, signature_B_fail1) = create_cooperative_settle_signatures(
        [A, B],
        channel_identifier,
        A, balance_A_fail1,
        B, balance_B_fail1
    )
    (signature_A_fail2, signature_B_fail2) = create_cooperative_settle_signatures(
        [A, B],
        channel_identifier,
        A, balance_A_fail2,
        B, balance_B_fail2
    )

    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A_fail1,
            B, balance_B_fail1,
            signature_A_fail1,
            signature_B_fail1
        )
    with pytest.raises(tester.TransactionFailed):
        token_network.transact({'from': C}).cooperativeSettle(
            channel_identifier,
            A, balance_A_fail2,
            B, balance_B_fail2,
            signature_A_fail2,
            signature_B_fail2
        )

    token_network.transact({'from': C}).cooperativeSettle(
        channel_identifier,
        A, balance_A,
        B, balance_B,
        signature_A,
        signature_B
    )


def test_update_channel_event(
        web3,
        get_accounts,
        token_network,
        create_channel,
        channel_deposit,
        create_cooperative_settle_signatures,
        event_handler
):
    ev_handler = event_handler(token_network)
    (A, B) = get_accounts(2)
    deposit_A = 10
    balance_A = 2
    balance_B = 8
    channel_identifier = create_channel(A, B)
    channel_deposit(channel_identifier, A, deposit_A)

    (signature_A, signature_B) = create_cooperative_settle_signatures(
        [A, B],
        channel_identifier,
        B, balance_B,
        A, balance_A
    )

    txn_hash = token_network.transact({'from': B}).cooperativeSettle(
        channel_identifier,
        B, balance_B,
        A, balance_A,
        signature_B,
        signature_A
    )

    ev_handler.add(txn_hash, E_CHANNEL_SETTLED, check_channel_settled(channel_identifier))
    ev_handler.check()
