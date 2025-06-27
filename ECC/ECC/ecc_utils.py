from tinyec import registry
import secrets
import hashlib

curve = registry.get_curve('brainpoolP256r1')

def encrypt_ECC(msg, pubKey):
    msg_bytes = msg.encode()
    privKey = secrets.randbelow(curve.field.n)
    sharedKey = privKey * pubKey
    sharedSecret = hashlib.sha256(int(sharedKey.x).to_bytes(32, 'big')).digest()
    cipher = bytes([m ^ k for m, k in zip(msg_bytes, sharedSecret)])
    return (privKey * curve.g, cipher)

def decrypt_ECC(encrypted_msg, privKey):
    pubKey, cipher = encrypted_msg
    sharedKey = privKey * pubKey
    sharedSecret = hashlib.sha256(int(sharedKey.x).to_bytes(32, 'big')).digest()
    plain = bytes([c ^ k for c, k in zip(cipher, sharedSecret)])
    return plain.decode()
