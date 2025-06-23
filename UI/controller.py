import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        medie = self._model.calcolaUmiditaMedieMese(self._view.dd_mese.value)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"L'umidita media nel mese selezionato è:"))
        for key, value in medie.items():
            self._view.lst_result.controls.append(ft.Text(f"{key}: {value}"))
        self._view.update_page()
        return

    def handle_sequenza(self, e):
        soluzioneOttima, costoOttimo = self._model.calcola_sequenza(self._view.dd_mese.value)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costoOttimo} ed è:"))
        for situazione in soluzioneOttima:
            self._view.lst_result.controls.append(ft.Text(f"{situazione}"))
        self._view.update_page()
        return


    def read_mese(self, e):
        self._mese = int(e.control.value)

