from debug import *
from zoodb import *
import rpclib
import time
import auth_client

def create(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('create', username=username)

def transfer(sender, recipient, zoobars, token):
    if not auth_client.check_token(sender, token):
        raise ValueError('invalid token')

    with rpclib.client_connect('/banksvc/sock') as c:
        c.call('transfer', sender=sender, recipient=recipient, zoobars=zoobars)
        transfer = Transfer()
        transfer.sender = sender
        transfer.recipient = recipient
        transfer.amount = zoobars
        transfer.time = time.asctime()

        transferdb = transfer_setup()
        transferdb.add(transfer)
        transferdb.commit()

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('balance', username=username)

def get_log(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('get_log', username=username)
