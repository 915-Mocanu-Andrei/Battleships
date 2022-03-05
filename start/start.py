from Battleships.ui.console import *

m1 = MRepo()
m2 = MRepo()
s1 = SRepo()
s2 = SRepo()
ser1 = Service(m1,s1)
ser2 = Service(m2,s2)
cons = Console(ser1,ser2)
cons.start()
