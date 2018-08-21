from neo.opcodes import OpCode

def main():
    a = OpCode.PUSHBYTES75.value
    print(OpCode.PUSHBYTES75.value[0])

if __name__ == "__main__":
    main()