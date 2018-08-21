class TransactionInput:
    """docstring for TransactionInput"""

    def __init__(self, hash = None, index = None):
        super(TransactionInput, self).__init__()
        self.assetid = hash
        self.value = index