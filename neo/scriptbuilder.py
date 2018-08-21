from core import BinaryWriter, BigInteger
from io import BytesIO
from neo import opcodes

class scriptbuilder:
    def __init__(self):
        super(scriptbuilder, self).__init__()
        self.bytesIO = BytesIO()
        self.writer = BinaryWriter(self.bytesIO)

    def toBytes(self):
        return self.bytesIO.getvalue()

    def Emit(self, opcode, arg = None):
        self.writer.WriteUInt8(opcode)
        if arg is not None:
            self.writer.WriteBytes(arg, False)
        return self

    def EmitAppCall(self, scriptHash, useTailCall):
        if len(scriptHash) != 20:
            raise RuntimeError('script hash length error')
        opcode = opcodes.OpCode.TAILCALL
        if not useTailCall:
            opcode = opcodes.OpCode.APPCALL
        return self.Emit(opcode, scriptHash)

    def EmitJump(self, opcode, offset):
        if opcode != opcodes.OpCode.JMP and opcode != opcodes.OpCode.JMPIF and opcode != opcodes.OpCode.JMPIFNOT and opcode != opcodes.OpCode.CALL:
            raise RuntimeError('opcode error')

        self.writer.WriteUInt8(opcode)
        self.writer.WriteUInt16(offset)
        return self

    def EmitPushNumber(self, num):
        if type(num) is int or type(num) is BigInteger:
            if num == -1:
                self.Emit(opcodes.OpCode.PUSHM1)
                return self
            if num == 0:
                self.Emit(opcodes.OpCode.PUSH0)
                return self
            if num > 0 and num < 16:
                self.Emit(opcodes.OpCode.PUSH1 - 1 + num)
                return self
            return self.EmitPushBytes(num.ToByteArray())

        return self

    def EmitPushBytes(self, bytes):
        length = len(bytes)
        if length <= opcodes.OpCode.PUSHBYTES75:
            self.writer.WriteUInt8(length)
            self.writer.WriteBytes(bytes, False)
        elif length < 0x100:
            self.Emit(opcodes.OpCode.PUSHDATA1)
            self.writer.WriteUInt8(length)
            self.writer.WriteBytes(bytes, False)
        elif length < 0x10000:
            self.Emit(opcodes.OpCode.PUSHDATA2)
            self.writer.WriteUInt16(length)
            self.writer.WriteBytes(bytes, False)
        else:
            self.Emit(opcodes.OpCode.PUSHDATA4)
            self.writer.WriteUInt32(length)
            self.writer.WriteBytes(bytes, False)
        return self

    def EmitPushString(self, data=''):
        d = bytearray(data.encode('utf-8'))
        return self.EmitPushBytes(d)

    def EmitSysCall(self, api=''):
        d = bytearray(api.encode('utf-8'))
        length = len(d)
        if length <= 0 or length > 252:
            raise RuntimeError('api length error')
        length_bytes = bytearray(length.to_bytes(1, 'little'))
        out = length_bytes + d
        return self.Emit(opcodes.OpCode.SYSCALL, out)

    def EmitPushBool(self, b):
        if b:
            self.Emit(opcodes.OpCode.PUSHT)
        else:
            self.Emit(opcodes.OpCode.PUSHF)

    def GetParamBytes(self, writer, str = ''):
        d = bytearray(str.encode('utf-8'))