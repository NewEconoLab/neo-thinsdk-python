from core import BinaryWriter
from io import BytesIO
import hashlib
from util.ec import verify
from util.bitcoin_utils import pubToAddress, getScriptFromPublicKey


class Transaction:
    txtype = None
    version = None
    attributes = []
    inputs = []
    outputs = []
    extdata = None

    """docstring for Transaction"""
    def __init__(self, txtype = None, version = None, inputs = [], outputs = [], attributes = [], extdata = None):
        """
        Create an instance.
        Args:
            inputs (list): of TransactionInput.
            outputs (list): of TransactionOutput items.
            attributes (list): of Attribute.
            extdata:
        """
        super(Transaction, self).__init__()
        self.inputs = inputs
        self.outputs = outputs
        self.Attributes = attributes
        self.scripts = extdata
        self.txtype = txtype
        self.version = version

    def GetMessage(self):
        bytesIO = BytesIO()
        writer = BinaryWriter(bytesIO)
        self.SerializeUnsigned(writer)
        return bytesIO.getvalue()

    def GetRawData(self):
        bytesIO = BytesIO()
        writer = BinaryWriter(bytesIO)
        self.Serialize(writer)
        return bytesIO.getvalue()

    def GetHash(self):
        bytesIO = BytesIO()
        writer = BinaryWriter(bytesIO)
        self.Serialize(writer)
        return bytesIO.getvalue()

    def AddWitness(self, signData, pubkey, addrs):
        bytesIO = BytesIO()
        writer = BinaryWriter(bytesIO)
        self.SerializeUnsigned(writer)
        data = bytesIO.getvalue()

        digest = hashlib.sha256(data).digest()
        ok = verify(digest, signData, pubkey)
        if not ok:
            return False
        addr = pubToAddress(pubkey)
        if addr != addrs:
            return False

        vscript = getScriptFromPublicKey(pubkey)

    def AddWitnessScript(self, script, iscript):
        pass

    def SerializeUnsigned(self, writer):
        pass

    def Serialize(self, writer):
        pass

    def Deserialize(self, reader):
        pass