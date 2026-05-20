import networkx as nx

from database.DAO import DAO
from model.genre import Genre


class Model:
    def __init__(self):
        self._graph = nx.MultiDiGraph()

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def buildGraph(self, genere: Genre):
        nodes = DAO.getAllNodes(genere)
        self._graph.add_nodes_from(nodes)
