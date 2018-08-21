from util import getScriptHashFromScript, getAddressFromScriptHash
import binascii

class Witness:
    """docstring for Witness"""

    def __init__(self, invocationscript = None, verificationscript = None):
        super(Witness, self).__init__()
        self.invocationscript = invocationscript
        self.verificationscript = verificationscript

    def GetAddress(self):
        hash = getScriptHashFromScript(self.verificationscript)
        address = getAddressFromScriptHash(hash)
        return address

    def GetHashStr(self):
        hash = getScriptHashFromScript(self.verificationscript)
        strHash = binascii.hexlify(hash)
        return strHash

    def IsSmartContract(self):
        if len(self.verificationscript) != 35:
            return True
        if self.verificationscript[0] != len(self.verificationscript) - 2:
            return True
        if self.verificationscript[len(self.verificationscript) - 1] != b'\xac':
            return True
        return False
