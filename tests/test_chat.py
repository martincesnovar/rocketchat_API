import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


def test_chat_post_update_delete_message(logged_rocket):
    chat_post_message = logged_rocket.chat_post_message(
        "hello", channel='GENERAL').json()
    assert chat_post_message.get('channel') == 'GENERAL'
    assert chat_post_message.get('message').get('msg') == 'hello'
    assert chat_post_message.get('success')

    with pytest.raises(RocketMissingParamException):
        logged_rocket.chat_post_message(text='text')

    msg_id = chat_post_message.get('message').get('_id')
    chat_get_message = logged_rocket.chat_get_message(msg_id=msg_id).json()
    assert chat_get_message.get('message').get('_id') == msg_id

    chat_update = logged_rocket.chat_update(room_id=chat_post_message.get('channel'),
                                            msg_id=chat_post_message.get(
                                                'message').get('_id'),
                                            text='hello again').json()

    assert chat_update.get('message').get('msg') == 'hello again'
    assert chat_update.get('success')

    chat_delete = logged_rocket.chat_delete(room_id=chat_post_message.get('channel'),
                                            msg_id=chat_post_message.get('message').get('_id')).json()
    assert chat_delete.get('success')


def test_chat_post_react(logged_rocket):
    message_id = logged_rocket.chat_post_message(
        "hello", channel='GENERAL').json().get('message').get('_id')
    chat_react = logged_rocket.chat_react(msg_id=message_id).json()
    assert chat_react.get('success')


def test_post_pin_unpin(logged_rocket):
    message_id = logged_rocket.chat_post_message(
        "hello", channel='GENERAL').json().get('message').get('_id')
    chat_pin_message = logged_rocket.chat_pin_message(message_id).json()
    assert chat_pin_message.get('success')
    assert chat_pin_message.get('message').get('t') == 'message_pinned'

    chat_unpin_message = logged_rocket.chat_unpin_message(message_id).json()
    assert chat_unpin_message.get('success')


def test_post_star_unstar(logged_rocket):
    message_id = logged_rocket.chat_post_message(
        "hello", channel='GENERAL').json().get('message').get('_id')
    chat_star_message = logged_rocket.chat_star_message(message_id).json()
    assert chat_star_message.get('success')

    chat_unstar_message = logged_rocket.chat_unstar_message(
        message_id).json()
    assert chat_unstar_message.get('success')


def test_chat_search(logged_rocket):
    chat_search = logged_rocket.chat_search(
        room_id='GENERAL', search_text='hello').json()
    assert chat_search.get('success')


def test_chat_get_message_read_receipts(logged_rocket):
    message_id = logged_rocket.chat_post_message(
        "hello", channel='GENERAL').json().get('message').get('_id')
    chat_get_message_read_receipts = logged_rocket.chat_get_message_read_receipts(
        message_id=message_id).json()
    assert chat_get_message_read_receipts.get('success')
    assert 'receipts' in chat_get_message_read_receipts
