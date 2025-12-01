import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        # TODO

        # Pulisco la listView
        self._view.lista_visualizzazione.controls.clear()

        if not self._view.guadagno_medio_minimo.value:
            return self._view.show_alert('Nessun valore inserito')
        try:
            guadagno_minimo=int(self._view.guadagno_medio_minimo.value)
            self._model.costruisci_grafo(guadagno_minimo)

            # costruisco il grafo con la soglia
            num_nodi = self._model.get_num_nodes()
            num_tratte = self._model.get_num_edges()
            edges = self._model.get_all_edges()

            self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di Hubs: {num_nodi}"))
            self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di Tratte: {num_tratte}"))

            for i, (u,v,peso) in enumerate(edges, start=1):
                hub1=self._model.hub[u]
                hub2=self._model.hub[v]
                self._view.lista_visualizzazione.controls.append(ft.Text(f"{i}) [{hub1} -> {hub2}] -- guadagno Medio Per spedizione: €{peso:,.2f}"))
        except ValueError:
            self._view.show_alert("Valore non valido")

        self._view.update()

