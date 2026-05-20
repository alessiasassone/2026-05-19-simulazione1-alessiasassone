import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        for g in self._model.getAllGeneri():
            self._view._ddGenre.options.append(ft.dropdown.Option(
                key = g.GenreId,
                text = g.Name,
                on_click = self._choiceDDGenere
            ))

    def _choiceDDGenere(self,e):
        self._choiceGenere = e.control.data
        print(f"Hai selezionato come genere {self._choiceGenere}")

    def handleCreaGrafo(self, e, genere):
        pass

    def handleCammino(self,e):
        pass