from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        # TODO
        self.G.clear() # svuoto il grafo

        # aggiungo i hub come nodi
        hubs=DAO.leggi_hub()
        for hub in hubs:
            self.G.add_node(hub.id)

        self.hub={h.id:h for h in hubs} # id di hub=chiave
                                        # h = valori info di hub

        # tratti
        tratte = DAO.get_spedizioni_media()
        for row in tratte:
            hub_min = row['origine']
            hub_max = row['destinazione']
            totale = float(row['somma_valore_merce'])
            n_spedizioni = int(row['num_spedizioni'])
            somma_media = totale / n_spedizioni if n_spedizioni > 0 else 0.0

            if somma_media >= threshold:
                self.G.add_edge(hub_min, hub_max, weight=somma_media)

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        # TODO
        return len(self.G.edges)

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        # TODO
        return len(self.G.nodes)

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        # TODO

        lista_archi=[]
        for u,v,data in self.G.edges(data=True):
            lista_archi.append((u,v,data['weight'])) # u= id primo arco
                                                     # v= id secondo arco
                                                     # data = dizionario attributi (somma_media)
        return lista_archi
