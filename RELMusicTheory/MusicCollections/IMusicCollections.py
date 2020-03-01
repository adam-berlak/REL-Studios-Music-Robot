import abc

class IMusicCollections(abc.ABC):

    @abc.abstractmethod
    def __eq__(self): pass

    @abc.abstractmethod
    def __str__(self): pass

    @abc.abstractmethod
    def __repr__(self): pass

    @abc.abstractmethod
    def __getitem__(self): pass

    @abc.abstractmethod
    def __contains__(self): pass

    @abc.abstractmethod
    def __add__(self, p_object): pass

    @abc.abstractmethod
    def __sub__(self, p_object): pass

    class IMusicIndex(abc.ABC):

        @abc.abstractmethod
        def __eq__(self): pass

        @abc.abstractmethod
        def __str__(self): pass

        @abc.abstractmethod
        def __repr__(self): pass

        @abc.abstractmethod
        def __add__(self, p_object): pass

        @abc.abstractmethod
        def __sub__(self, p_object): pass

        @abc.abstractmethod
        def distanceFrom(self, p_object): pass

        @abc.abstractmethod
        def distanceFromNext(self, p_object): pass

        @abc.abstractmethod
        def build(self, p_item_1, p_item_2): pass

        @abc.abstractmethod
        def getPosition(self): pass

        @abc.abstractmethod
        def next(self): pass

        @abc.abstractmethod
        def previous(self): pass

class MusicCollections(IMusicCollections):

    def __init__(self, p_pitched_object, p_intervals):
        self.pitched_object = p_item_1
		self.parent_degree = None
		self.indices = []

		for i in range(len(p_intervals)): self.indices.append(type(self)._MusicIndex(p_intervals[i], self))

    class _MusicIndex(IMusicCollections.IMusicIndex):
