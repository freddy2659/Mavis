from pathlib import Path


class Beacons:

    def __init__(self, defaultSig='sig.png'):
        self.dict = dict()
        self.sig = defaultSig
        return
        
    def addBeacon(self, id):
        if id in self.dict:
            print("Tried to add an existing beacon")
        else:
            self.dict[id] = Beacon(id)
        return
        
    def setDefaultSig(self, sig):
        self.sig = sig
        return
        
        
class Beacon:

    def __init__(self, id):
        self._enabled = True
        self.id = id
        self.count = 0
        self.ipList = []
        return
        
    def __str__(self):
        return f"ID: {self.id}, Visits: {self.count}, IPs: {self.ipList}"
        
    def visit(self, ip):
        self.count = self.count + 1
        self.ipList.append(ip)
        return
        
    def isEnabled(self):
        return self._enabled
        
    def remove(self):
        self._enabled = False
        return
