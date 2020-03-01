import abc

class IPitchedObject(abc.ABC):

    @abc.abstractmethod
    def __eq__(self): pass

    @abc.abstractmethod
    def __str__(self): pass

    @abc.abstractmethod
    def __repr__(self): pass

    @abc.abstractmethod
    def __add__(self, p_object): 
        '''
        Must handle Cases:
        isinstance(p_object, Interval): return type(self)
        >>> Tone("C", 0) + M3
        "E"
        '''
        pass

    @abc.abstractmethod
    def __sub__(self, p_object): 
        '''
        Must handle Cases:
        Case: isinstance(p_object, Interval)
        Return: type(self) Object
        >>> Tone("C", 0) - m3
        "A"
        Case: isinstance(p_object, type(self)) 
        Return: Interval Object
        >>> Tone("C", 0) - Tone("A", 0)
        "b3"
        '''
        pass

    @abc.abstractmethod
    def build(self): 
        '''
        Allows you to build a complex MusicObject off of a PitchedObject
        >>> Tone("C", 0).build(Scale, major)
        "<Scale I=C, ii=D, iii=E, IV=F, V=G, vi=A, vii=B>"
        '''
        pass

    @abc.abstractmethod
    def simplify(self): 
        '''
        Allows for normalization of PitchedObject, used in comparison
        >>> Tone("C", -3).simplify()
        "A"
        >>> Tone("C", -4).simplify()
        ["A#", "Bb"]
        '''
        pass

    @abc.abstractmethod
    def getTone(self): 
        '''
        Used for getting Tone componant of PitchedObject
        >>> Key(Tone("C", 0), 4).getTone()
        "C"
        >>> Key(Tone("C", 0), 4).getTone() == Key(Tone("C", 0), 5).getTone()
        True
        '''
        pass