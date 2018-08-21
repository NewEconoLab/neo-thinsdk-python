class TransactionOutput:
    """docstring for TransactionOutput"""

    def __init__(self, assetid = None, value = None, address = None):
        super(TransactionOutput, self).__init__()
        self.assetid = assetid
        self.value = value
        self.address = address