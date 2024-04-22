import hashlib
import string
import random

def hash_pwd(password):
    salt = "".join(random.choices(string.hexdigits, k=32))
    salted_password = (password + salt).encode("utf-8")
    hash_object = hashlib.sha256(salted_password)
    hashed_password = hash_object.hexdigest()
    return hashed_password, salt

def check_pwd(password, saved_password_hash, salt):
    salted_password = (password + salt).encode("utf-8")
    hash_object = hashlib.sha256(salted_password)
    hashed_password = hash_object.hexdigest()
    return hashed_password == saved_password_hash

def test_hash_password():
    hashed_password, salt = hash_pwd("password")
    assert type(hashed_password) is str
    assert type(salt) is str
    assert check_pwd("passwordx", hashed_password, salt) == False
    assert check_pwd("password", hashed_password, salt) == True

if __name__ == "__main__":
    test_hash_password()
    print("done")