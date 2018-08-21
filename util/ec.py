import hashlib
import os
import ecdsa
from ecdsa import ellipticcurve
from ecdsa.util import string_to_number, number_to_string2
from util.bitcoin_utils import hash_160_to_bc_address, hash_160, encodebase58check, wiftosecret
from util.key_formatting import decode_pubkey


def GetPubKey(pubkey, compressed=False):
    # public keys are 65 bytes long (520 bits)
    # 0x04 + 32-byte X-coordinate + 32-byte Y-coordinate
    # 0x00 = point at infinity, 0x02 and 0x03 = compressed, 0x04 = uncompressed
    # compressed keys:
    # <sign> <x> where <sign> is 0x02 if y is even and 0x03 if y is odd
    if compressed:
        if pubkey.point.y() & 1:
            key = '03' + '%064x' % pubkey.point.x()
        else:
            key = '02' + '%064x' % pubkey.point.x()
    else:
        key = '04' + \
              '%064x' % pubkey.point.x() + \
              '%064x' % pubkey.point.y()
    return bytes.fromhex(key)

def toUncompressed(compressedpubkey):
    return decode_pubkey(compressedpubkey, 'bin_compressed')

def toPoint( x, y):
    return ellipticcurve.Point(ecdsa.ecdsa.generator_256.curve(), x, y, ecdsa.ecdsa.generator_256.order())

def verifyKeyFromPoint(p):
    return ecdsa.ecdsa.VerifyingKey.from_public_point(p, ecdsa.NIST256p, hashlib.sha256)

def verify(digest, signature, pub):
    x, y = toUncompressed(pub)
    point = toPoint(x, y)
    verifyKey = verifyKeyFromPoint(point)
    return verifyKey.verify_digest(
        signature, digest, sigdecode=ecdsa.util.sigdecode_string)

class EC_KEY(object):
    def __init__(self, secret):
        self.pubkey = ecdsa.ecdsa.Public_key(
            ecdsa.ecdsa.generator_256,
            ecdsa.ecdsa.generator_256 * secret
        )
        self.privkey = ecdsa.ecdsa.Private_key(self.pubkey, secret)
        self.secret = secret

    @classmethod
    def from_wif(klass, wif):
        b = wiftosecret(wif, 0)
        if not b:
            return False
        b = b[0:32]
        #secret = int('0x' + b.encode('hex'), 16)
        secret = string_to_number(b);
        return EC_KEY(secret)

class EllipticCurveKey:

    def __init__(self):
        self._secret = None
        self._private_key = None
        self._public_key = None

    def new_key_pair(self):
        secret = os.urandom(32)
        self.set_secret(secret)

    def set_secret(self, secret):
        self._secret = secret
        secret = string_to_number(secret)
        pkey = EC_KEY(secret)

        secexp = pkey.secret
        self._private_key = ecdsa.SigningKey.from_secret_exponent(
            secexp, curve= ecdsa.NIST256p)
        self._public_key = self._private_key.get_verifying_key()

    def sign(self, digest):
        if self._private_key is None:
            return None
        return self._private_key.sign_digest_deterministic(
            digest, hashfunc=hashlib.sha256,
            sigencode=ecdsa.util.sigencode_string)

    def verify(self, digest, signature):
        if self._public_key is None:
            return None
        return self._public_key.verify_digest(
            signature, digest, sigdecode=ecdsa.util.sigdecode_string)

    @property
    def secret(self):
        return self._secret

    @property
    def public_key(self):
        return GetPubKey(self._public_key.pubkey, True)

    @property
    def uncompressed_public_key(self):
        return GetPubKey(self._public_key.pubkey, False)

    @property
    def script(self):
        vchIn = bytes([33])
        vchIn += self.public_key
        vchIn += bytes([172])
        return vchIn

    @property
    def key_id(self):
        return hash_160(self.script)

    @property
    def address(self):
        return hash_160_to_bc_address(0x17, self.key_id)

    @property
    def wif(self):
        vchIn = bytes([(0 + 128) & 255])
        vchIn += secret
        vchIn += bytes([0x01])
        return encodebase58check(vchIn)

if __name__ == "__main__":
    ec = EllipticCurveKey()
    ec.new_key_pair()
    sig = ec.sign(b"123")
    secret = ec.secret
    print(secret)
    print(len(secret))
    print(len(sig))
    print(ec.public_key)
    print(len(ec.public_key))
    print(ec.address)
    print(ec.wif)

    ec_key = EC_KEY.from_wif("L4RmQvd6PVzBTgYLpYagknNjhZxsHBbJq4ky7Zd3vB7AguSM7gF1")
    ec2 = EllipticCurveKey()
    s = number_to_string2(ec_key.secret, 32)
    ec2.set_secret(s)
    print(ec2.public_key)
    print(ec2.uncompressed_public_key)
    print(ec2.address)
    aa, bb = toUncompressed(ec2.public_key)
    print(aa, bb)
    cc = toPoint(aa, bb)

    pubkey = ecdsa.ecdsa.Public_key(ecdsa.ecdsa.generator_256, cc)
    dd = GetPubKey(pubkey, True)
    print(dd)
    ee = GetPubKey(pubkey, False)
    print(ee)
    assert ec.verify(b"123", sig)

