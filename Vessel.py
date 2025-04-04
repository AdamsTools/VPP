import numpy as np





class Vessel():
    def __init__(self, loa, lwl, draft, beam):

        self.LOA = loa
        self.lwl = lwl
        self.draft = draft
        self.beam = beam

    def hull(self):
        None

class Rudder():
    def __init__(self, span):
        self.span = span



class Keel():
    def __init__(self, span):
        self.span = span


class Propeller():
    def __init__(self, blades):
        self.blades = blades


class Sail():

    def __init__(self):
        None
    
    def mainsail(self):
        None

    def genoa(self):
        None

    def spinakker(self):
        None

    def genakker(self):
        None

    class Mast():
        def __init__(self):
            None

        def spar(self):
            None
