from enum import Enum

class AttributeType(Enum):
    #< summary >
    # 外部合同的散列值
    # < / summary >
    ContractHash = b'\x00'
    # < summary >
    # 用于ECDH密钥交换的公钥，该公钥的第一个字节为0x02
    # < / summary >
    ECDH02 = b'\x02'
    # < summary >
    # 用于ECDH密钥交换的公钥，该公钥的第一个字节为0x03
    # < / summary >
    ECDH03 = b'\x03'

    # < summary >
    # 用于对交易进行额外的验证
    # < / summary >
    Script = b'\x20'

    Vote = b'\x30'

    DescriptionUrl = b'\x81'
    Description = b'\x90'

    Hash1 = b'\xa1'
    Hash2 = b'\xa2'
    Hash3 = b'\xa3'
    Hash4 = b'\xa4'
    Hash5 = b'\xa5'
    Hash6 = b'\xa6'
    Hash7 = b'\xa7'
    Hash8 = b'\xa8'
    Hash9 = b'\xa9'
    Hash10 = b'\xaa'
    Hash11 = b'\xab'
    Hash12 = b'\xac'
    Hash13 = b'\xad'
    Hash14 = b'\xae'
    Hash15 = b'\xaf'

    # < summary >
    # 备注
    # < / summary >
    Remark = b'\xf0'
    Remark1 = b'\xf1'
    Remark2 = b'\xf2'
    Remark3 = b'\xf3'
    Remark4 = b'\xf4'
    Remark5 = b'\xf5'
    Remark6 = b'\xf6'
    Remark7 = b'\xf7'
    Remark8 = b'\xf8'
    Remark9 = b'\xf9'
    Remark10 = b'\xfa'
    Remark11 = b'\xfb'
    Remark12 = b'\xfc'
    Remark13 = b'\xfd'
    Remark14 = b'\xfe'
    Remark15 = b'\xff'