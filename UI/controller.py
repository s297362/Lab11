import flet as ft

import database.DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        anni = [2015, 2016, 2017, 2018]
        for i in anni:
            self._view._ddyear.options.append(ft.dropdown.Option(key = i, text = str(i)))
        colori = database.DAO.DAO().getColori()
        colori = sorted(colori, key=lambda x: x.Product_color)
        for c in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(key=c.Product_color, text=c.Product_color))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txtOut.clean()
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value
        self.graph = self._model.buildGraph(colore, int(anno))
        self._view.txtOut.controls.append(ft.Text(f'Numero nodi: {len(self.graph.nodes)}\nNumero archi: {len(self.graph.edges(data=True))}'))
        archi_ordinati = sorted(self.graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        i = 0
        archi_ripetuti = []
        for a in archi_ordinati:
            i += 1
            if i < 4:
                archi_ripetuti.append(a[0])
                archi_ripetuti.append(a[1])
                self._view.txtOut.controls.append(ft.Text(f'Arco da {a[0]} a {a[1]}, peso={a[2]['weight'][0]}'))
        a = []
        for b in archi_ripetuti:
            if archi_ripetuti.count(b) > 1:
                archi_ripetuti.remove(b)
                a.append(b)
        self._view.txtOut.controls.append(ft.Text(f'Nodi ripetuti: {a}'))
        self.fillDDProduct()
        self._view.update_page()


    def fillDDProduct(self):
        orderedNodes = sorted(self.graph.nodes, key=lambda x: self._model.idMap[x].Product_number)
        for nodo in orderedNodes:
            self._view._ddnode.options.append(ft.dropdown.Option(key=self._model.idMap[nodo].Product_number, text=self._model.idMap[nodo].Product_number))
        self._view.update_page()

    def handle_search(self, e):
        nodo = self._view._ddnode.value
        soluzione = self._model.percorsoOttimo(int(nodo))
        self._view.txtOut2.controls.append(ft.Text(f'Lunghezza in numero di archi {soluzione} {self._model.lenOttima}'))
        self._view.update_page()
