import abc

class IMusicObject(abc.ABC):

    @abc.abstractmethod
    def __play__(self):
        pass

    @abc.abstractmethod
    def __toMidiData__(self):
        pass