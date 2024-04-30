import copy
from datetime import datetime

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.possibili_soluzioni = []



    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, set(self._listEvents))
        #print(self.possibili_soluzioni)
        self._solBest = self.get_max()
        print(self._solBest)

    def ricorsione(self, parziale, maxY, maxH, eventi_rimanenti):
        # TO FILL
        if len(eventi_rimanenti) == 0:
            self.possibili_soluzioni.append(copy.deepcopy(parziale))
            #print(parziale)
        else:
            for event in eventi_rimanenti:
                if self.filtro(event, parziale, maxY, maxH):
                    parziale.append(event)
                    new_eventi_rimanenti = copy.deepcopy(eventi_rimanenti)
                    new_eventi_rimanenti.remove(event)
                    #print(parziale)
                    self.ricorsione(parziale, maxY, maxH, new_eventi_rimanenti)
                    parziale.pop()
                else:
                    self.possibili_soluzioni.append(copy.deepcopy(parziale))



    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

    def filtro(self, evento, parziale, maxY, maxH):
        durata_tot = 0
        for event in parziale:
            durata_tot += event.durata.seconds
        durata_tot += evento.durata.seconds
        if durata_tot > (maxH * 3600):
            return False

        min_data = datetime(2015, 1, 1, 0, 0, 0)
        for event in parziale:
            if event._date_event_began < min_data:
                min_data = event._date_event_began
        durata_anni = evento._date_event_finished - min_data
        if durata_anni.seconds > (maxY * 365 * 24 * 3600):
            return False

        return True

    def get_max(self):
        max_colpiti = 0
        best_soluzioni = ()
        for soluzione in self.possibili_soluzioni:
            colpiti = 0
            for event in soluzione:
                colpiti += event.customers_affected
            if colpiti > max_colpiti:
                max_colpiti = colpiti
                best_soluzioni = (soluzione, colpiti)

        return best_soluzioni
