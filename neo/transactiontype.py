from enum import Enum

class TransactionType(Enum):
    MinerTransaction = b'\x00'
    IssueTransaction = b'\x01'
    ClaimTransaction = b'\x02'
    EnrollmentTransaction = b'\x20'
    RegisterTransaction = b'\x40'
    ContractTransaction = b'\x80'
    PublishTransaction = b'\xd0'
    InvocationTransaction = b'\xd1'