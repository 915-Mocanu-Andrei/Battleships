from dataclasses import dataclass


@dataclass
class Ship:
    _status:int
    _length:int
    _cells:list
    _marks:int

    @property
    def cells(self):
        return self._cells

    @property
    def length(self):
        return self._length

    @property
    def marks(self):
        return self._marks

    @property
    def status(self):
        return self._status

    @marks.setter
    def marks(self,markss):
        self._marks = markss

    @length.setter
    def length(self, lengths):
        self._length = lengths

    @cells.setter
    def cells(self, s_cels):
        self._cells = s_cels

    def add_cell(self,cell):
        self._cells.append(cell)

    @status.setter
    def status(self, statuss):
        self._status = statuss
