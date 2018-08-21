class CreateSignParams:
    """docstring for CreateSignParams"""
    txtype = None
    version = None
    prikey = None
    fromaddr = None
    toaddr = None
    assetid = None
    value = 0
    data = []
    utxos = []

    def __init__(self, txtype = None, version = None, prikey = None, fromaddr = None, toaddr = None, assetid = None,
                 value = 0, data = [], utxos = []):
        super(CreateSignParams, self).__init__()
        self.txtype = txtype
        self.version = version
        self.prikey = prikey
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.assetid = assetid
        self.value = value
        self.data = data
        self.utxos = utxos