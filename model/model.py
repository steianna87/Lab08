import copy
from datetime import datetime
from time import time

from database.DAO import DAO
from model.insieme_eventi import InsiemeEventi


class Model:
    def __init__(self):
        self._solBest = None
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.possibili_soluzioni = set()
        self.chiamate_finali = 0
        self.ricorsioni = 0

    def worstCase(self, nerc, maxY, maxH):
        self.possibili_soluzioni = set()
        self._solBest = None
        self.chiamate_finali = 0
        self.ricorsioni = 0
        # TO FILL
        self.loadEvents(nerc)
        #self._listEvents.sort(key=lambda c: c.durata, reverse=True)
        for event in self._listEvents:
            print(event)
        t1 = time()
        self.ricorsione([], maxY, maxH, 0)
        t2 = time()
        print(f"Possibili Soluzioni:\n"
              f"{self.possibili_soluzioni}")
        #self._solBest = self.get_max()
        print(f"Migliore soluzione:\n"
              f"{self._solBest}")

        print(self.ricorsioni)
        print(self.chiamate_finali)
        print(f'Tempo impiegato: {t2-t1}')

    def ricorsione(self, parziale, maxY, maxH, pos):
        self.ricorsioni += 1

        parziale = InsiemeEventi(parziale)
        eventi_rimanenti = InsiemeEventi(self._listEvents[pos:])
        if (self._solBest is not None and
                eventi_rimanenti.tot_persone_coinvolte + parziale.tot_persone_coinvolte <
                self._solBest.tot_persone_coinvolte):
            return
        # TO FILL
        if pos == len(self._listEvents):
            self.chiamate_finali += 1
            if self._solBest is None:
                self._solBest = parziale
            else:
                if parziale.tot_persone_coinvolte > self._solBest.tot_persone_coinvolte:
                    self._solBest = parziale
            '''presente = False
            for sol in self.possibili_soluzioni:
                if sol.eventi == parziale.eventi:
                    presente = True
                    break
            if not presente:
                self.possibili_soluzioni.add(InsiemeEventi(parziale.eventi))'''
        else:

            for event in self._listEvents[pos:]:
                pos += 1
                if self.filtro(event, parziale.eventi, maxY, maxH):
                    parziale.add_evento(event)
                    print(parziale)
                    self.ricorsione(parziale.eventi, maxY, maxH, pos)
                    parziale.remove_evento(event)

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
            durata_tot += event.durata.total_seconds()
        durata_tot += evento.durata.total_seconds()
        if durata_tot > (maxH * 3600):
            return False

        min_data = datetime(2015, 1, 1, 0, 0, 0)
        for event in parziale:
            if event._date_event_began < min_data:
                min_data = event._date_event_began
        durata_anni = evento._date_event_finished - min_data
        if durata_anni.total_seconds() > (maxY * 365 * 24 * 3600):
            return False

        return True

    def get_max(self):
        max_colpiti = 0
        best_soluzioni = None
        for soluzione in self.possibili_soluzioni:
            colpiti = 0
            for event in soluzione.eventi:
                colpiti += event.customers_affected
            if colpiti > max_colpiti:
                max_colpiti = colpiti
                best_soluzioni = soluzione

        return best_soluzioni
