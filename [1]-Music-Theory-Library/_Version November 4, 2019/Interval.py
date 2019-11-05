# Class Name: Interval
# Parameters: p_semitones (Number of Semitones in interval), p_numeral (numeral representation), p_accidental (sharp/flat)
class Interval:
	def __init__(self, p_semitones, p_numeral, p_accidental=""):
		self.semitones = p_semitones
		self.numeral = p_numeral
		self.accidental = p_accidental
	def __str__(self):
		return str(self.getNumeral()) + self.getAccidental()
	def __eq__(self, p_other):
		return self.getSemitones() == p_other.getSemitones()
	def __add__(self, p_other):
		if (isinstance(p_other, Interval)):
			return self.getSemitones() + p_other.getSemitones()
		if (isinstance(p_other, int)):
			return self.getSemitones() + p_other
		if (isinstance(p_other, str)):
			return self.__str__() + p_other
	def __radd__(self, p_other):
		if (isinstance(p_other, int)):
			return self.getSemitones() + p_other
		if (isinstance(p_other, str)):
			return p_other + self.__str__() 
	def __sub__(self, p_other):
		if (isinstance(p_other, Interval)):
			return self.getSemitones() - p_other.getSemitones()
		if (isinstance(p_other, int)):
			return self.getSemitones() - p_other
		
	def setSemitones(self, p_semitones):
		self.semitones = p_semitones
	def setNumeral(self, p_numeral):
		self.numeral = p_numeral
	def setAccidental(self, p_accidental):
		self.accidental = p_accidental
	def setAccidental(self, p_accidental):
		self.accidental = p_accidental
		
	def getSemitones(self):
		return self.semitones
	def getNumeral(self):
		return self.numeral
	def getAccidental(self):
		return self.accidental
	def getAccidental(self):
		return self.accidental