import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # TO FILL
        global max_anni, max_ore

        self._view._txtOut.controls = []

        nerc = self._view._nerc
        if nerc is None:
            self._view.create_alert('Selezionare un NERC')
        else:
            try:
                max_anni = int(self._view._txtYears.value)
                max_ore = int(self._view._txtHours.value)
                self._model.worstCase(nerc, max_anni, max_ore)
                self._view._txtOut.controls.append(ft.Text(self._model._solBest))
                self._view.update_page()

            except ValueError:
                self._view.create_alert('Inserire dei numeri')


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
