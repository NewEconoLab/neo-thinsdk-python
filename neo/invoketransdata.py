from neo import IExtData
from core import Fixed8


class InvokeTransData(IExtData):
    """docstring for InvokeTransData"""
    script = []
    gas = None

    def __init__(self, script=None, gas=None):

        super(InvokeTransData, self).__init__()
        self.script = script
        self.gas = gas

    def serialize(self, version, writer):
        '''
        serialize
        '''
        writer.WriteVarBytes(self.script)
        if version >= 1:
            writer.WriteUInt64(self.gas.value)

    def deserialize(self, version, reader):
        '''
        deserialize
        '''
        self.script = reader.ReadVarBytes()
        if version >= 1:
            self.gas = Fixed8()
            self.gas.value = reader.ReadUInt8()
