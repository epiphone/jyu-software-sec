from zoodb import *
from debug import *

import auth_client
import time

def create(username):
    db = bank_setup()
    bank = Bank(username=username)
    db.add(bank)
    db.commit()

def transfer(sender, recipient, zoobars):
    bank_db = bank_setup()
    sender_bank = _get_bank(bank_db, sender)
    recipient_bank = _get_bank(bank_db, recipient)

    sender_balance = sender_bank.zoobars - zoobars
    recipient_balance = recipient_bank.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    sender_bank.zoobars = sender_balance
    recipient_bank.zoobars = recipient_balance
    bank_db.commit()

def balance(username):
    bank = _get_bank(bank_setup(), username)
    return bank.zoobars

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

def _get_bank(db, username):
    return db.query(Bank).get(username)
