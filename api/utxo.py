class Utxo:
    """docstring for Utxo"""

    def __init__(self, hash = None, value = None, n = None):
        super(Utxo, self).__init__()
        self.hash = hash
        self.value = value
        self.n = n