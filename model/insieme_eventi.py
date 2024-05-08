import copy
import datetime


class InsiemeEventi():
    def __init__(self, eventi):
        self.eventi = copy.deepcopy(set(eventi))
        self.tot_persone_coinvolte = self.get_tot_persone_coinvolte()
        self.tot_ore = self.get_tot_ore()

    def get_tot_persone_coinvolte(self):
        tot_coinvolti = 0
        for event in self.eventi:
            tot_coinvolti += event.customers_affected
        return tot_coinvolti

    def get_tot_ore(self):
        tot_ore = datetime.timedelta(0.0)
        for event in self.eventi:
            tot_ore += event.durata
        return tot_ore.total_seconds() / 3600

    def get_min_durata(self):
        min = 1e16
        event_min = None
        for event in self.eventi:
            if event.durata.total_seconds() / 3600 < min:
                min = event.durata.total_seconds() / 3600
                event_min = event
        return min

    def aggiorna_coinvolti(self):
        self.tot_persone_coinvolte = self.get_tot_persone_coinvolte()
        self.tot_ore = self.get_tot_ore()

    def add_evento(self, evento):
        self.eventi.add(evento)
        self.aggiorna_coinvolti()

    def remove_evento(self, evento):
        self.eventi.remove(evento)
        self.aggiorna_coinvolti()

    def __str__(self):
        risultato = (f"Totale coinvolti: {self.tot_persone_coinvolte}\n"
                    f"Totale ore: {self.tot_ore}\n")
        for event in self.eventi:
            risultato += f'{event} \n'

        return risultato

    def __repr__(self):
        return (f"Eventi: {self.eventi}\n"
                f"Totale coinvolti: {self.tot_persone_coinvolte}\n"
                f"Totale ore: {self.tot_ore}\n")
