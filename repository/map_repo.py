
"""x=input('')
print(ord(x)-ord('a'))"""
import numpy


class MRepo:
    def __init__(self):
        self._matrix=[[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0]]
        # self._matrix = numpy.zeros((10, 10))
        self._hit = 0
        self._miss = 0
        #0 means empty
        #1 means part of a functional ship
        #2 means miss
        #3 means hit

    def get_cell_status(self,line,column):
        return self._matrix[line][column]

    def change_cell_status(self,line,column,status):
        self._matrix[line][column] = status

    def get_repo(self):
        return self._matrix

    @property
    def hits(self):
        return self._hit

    @property
    def misses(self):
        return self._miss

    @hits.setter
    def hits(self,hit):
        self._hit = hit

    @misses.setter
    def misses(self,miss):
        self._miss = miss
