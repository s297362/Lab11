import copy

import networkx as nx

import database.DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}
        self.bestSol = []
        self.lenOttima = 0

    def buildGraph(self, colore, anno):
        prodotti = database.DAO.DAO().getProdotti(colore)
        for p in prodotti:
            self.graph.add_node(p.Product_number)
            self.idMap[p.Product_number] = p
        for n1 in self.graph.nodes:
            for n2 in self.graph.nodes:
                if n1 != n2 and database.DAO.DAO().getArchi(n1, n2, anno)[0] > 0:
                    self.graph.add_edge(n1, n2, weight=database.DAO.DAO().getArchi(n1, n2, anno))
        return self.graph

    def percorsoOttimo(self, nodo):
        self.ricorsione([nodo], self.graph.nodes)
        return self.bestSol

    def ricorsione(self, parziale, nodi):
        # Condizione terminale
        if self.is_soluzione(parziale):
            if len(parziale) > self.lenOttima:
                self.bestSol.append(copy.deepcopy(parziale))
                self.lenOttima = len(parziale)
        else:
            for n in nodi:
                if self.graph.has_edge(parziale[-1], n):
                    parziale.append(n)
                    self.ricorsione(parziale, nodi)
                    parziale.pop()

    def is_soluzione(self, parziale):
        if len(parziale) < 3:
            return False
        if self.graph[parziale[-2]][parziale[-1]]['weight'] < self.graph[parziale[-3]][parziale[-2]]['weight']:
            return False
        return True

