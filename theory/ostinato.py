from theory.chord import *

class Ostinato:

    def __init__(self, p_chord, p_pattern):
        self.chord = p_chord
        self.pattern = p_pattern

    def repr_BL(self):
        return self.str_BL(self)

    def str_BL(self):
        items = [self.get_chord().getitem_BL(item) for item in self.get_pattern()]
        items2 = [[]]
        counter = 0

        for item in items:
            x_coord = counter
            y_coord = item.get_generic_interval_BL().get_numeral()

            while len(items2) <= y_coord: items2.append([])

            for i in range(len(items2)):
                while len(items2[i]) <= x_coord: items2[i].append('___________')

            items2[y_coord][x_coord] = ('(' + str(item) + ')').ljust(11).replace(' ', '_')
            counter += 1

        return '\n'.join([''.join([str(item) for item in row]) for row in items2[::-1]])

    def __repr__(self):
        return self.repr_BL()

    def __str__(self):
        return self.str_BL()

    def transpose_BL(self, p_index):
        new_ostinato = Ostinato(self.get_chord().transpose_BL(p_index), self.get_pattern())
        return new_ostinato

    def get_chord(self):
        return self.chord
    
    def get_pattern(self):
        return self.pattern