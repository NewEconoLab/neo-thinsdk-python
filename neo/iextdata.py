import abc

class IExtData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serialize(self, version, writer):
        '''
        serialize
        '''

    @abc.abstractmethod
    def deserialize(self, version, reader):
        '''
        deserialize
        '''