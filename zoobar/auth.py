from zoodb import *
from debug import *

import base64
import hashlib
import os
import pbkdf2
import random

HASH_LEN = 32
SALT_LEN = 10

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = _get_cred(db, username)
    if not cred:
        return None
    if _hash_password(password, cred.salt) == cred.password:
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    # Check for existing cred:
    db = cred_setup()
    if _get_cred(db, username):
        return None

    # Create a new one:
    newcred = Cred()
    newcred.username = username
    newcred.salt = base64.b64encode(os.urandom(SALT_LEN))
    newcred.password = _hash_password(password, newcred.salt)
    db.add(newcred)
    db.commit()
    return newtoken(db, newcred)

def check_token(username, token):
    cred = _get_cred(cred_setup(), username)
    return cred and cred.token == token

def _get_cred(db, username):
  return db.query(Cred).get(username)

def _hash_password(password, salt):
  return pbkdf2.PBKDF2(password, salt).hexread(HASH_LEN)
