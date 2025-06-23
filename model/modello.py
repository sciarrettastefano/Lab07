import copy
from unittest import case

from mysql.opentelemetry.importlib_metadata import pass_none

from database.meteo_dao import MeteoDao

class Model:

    def __init__(self):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []

        self.umiditaMedieMeseSelezionato = {"Genova": 0,
                                            "Milano": 0,
                                            "Torino": 0}


    def calcolaUmiditaMedieMese(self, mese):
        self.umiditaMedieMeseSelezionato = {"Genova": 0,
                                            "Milano": 0,
                                            "Torino": 0}
        totGen = 0
        totMil = 0
        totTor = 0
        genCounter = 0
        milCounter = 0
        torCounter = 0
        allSituazioni = MeteoDao.get_all_situazioni_mese(mese)
        for s in allSituazioni:
            match s.localita:
                case "Genova":
                    genCounter += 1
                    totGen += s.umidita
                case "Milano":
                    milCounter += 1
                    totMil += s.umidita
                case "Torino":
                    torCounter += 1
                    totTor += s.umidita

        try:
            self.umiditaMedieMeseSelezionato["Genova"] = round(totGen/genCounter, 4)
            self.umiditaMedieMeseSelezionato["Milano"] = round(totMil/milCounter, 4)
            self.umiditaMedieMeseSelezionato["Torino"] = round(totTor/torCounter, 4)
        except ZeroDivisionError:
            print("Divsione per 0 impossibile")
            return
        print(self.umiditaMedieMeseSelezionato["Genova"])
        print(self.umiditaMedieMeseSelezionato["Milano"])
        print(self.umiditaMedieMeseSelezionato["Torino"])
        return self.umiditaMedieMeseSelezionato


    def calcola_sequenza(self, mese):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao.get_all_situazioni_meta_mese(mese)
        self._ricorsione([], situazioni)
        return self.soluzione_ottima, self.costo_ottimo # ----> struttura utile per I/O


    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale)+1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati


    def is_admissible(self, candidate, parziale):
        # vincolo 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False
        # vincolo su permanenza
        # 1) lunghezza di parziale < 3
        if len(parziale) == 0:
            return True

        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False
        # 2) le tre localita precedenti non sono tutte uguali
        else:
            if parziale[-1].localita != parziale[-2].localita or parziale[-1].localita != parziale[-3].localita or parziale[-2].localita != parziale[-3].localita:
                if parziale[-1].localita != candidate.localita:
                    return False
        # altrimenti ok
        return True


    def _calcola_costo(self, parziale):
        costo = 0
        # 1) costo umidita
        for situazione in parziale:
            costo += situazione.umidita

        # 2) costo su spostamenti
        for i in range(len(parziale)):
            # se i due giorni precedenti non sono stato nella
            # stessa citta in cui sono ora, pago 100
            if i >=2 and (parziale[i-1].localita != parziale[i].localita or
                          parziale[i-2].localita != parziale[i].localita):
                costo += 100

        return costo


    def _ricorsione(self, parziale, lista_situazioni):
        #condizione terminale
        if len(parziale) == 15:
            self.n_soluzioni += 1
            costo = self._calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)

            # pass
        #condizione ricorsiva
        else:
            #cercare le città per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale, lista_situazioni)
            #provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                #verifica vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()



if __name__ == '__main__':
    my_model = Model()
    print(my_model.calcola_sequenza(2))
    #print(f"N soluzioni: {my_model.n_soluzioni}")
