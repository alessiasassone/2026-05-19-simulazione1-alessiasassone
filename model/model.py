import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO
from model.genre import Genre


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getArtists(self):
        return self._graph.nodes()

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def buildGraph(self, genere: Genre):

        self._graph.clear()
        self._idMap.clear()

        nodes = DAO.getAllNodes(genere)
        for node in nodes:
            self._idMap[node.ArtistID] = node

        self._graph.add_nodes_from(nodes)

        custom_artist_list = DAO.getCustomerArtistCounts(genere)

        customer_artists = defaultdict(set)
        artist_popularity = defaultdict(int)

        for customer_id, artist_id, ntracks in custom_artist_list:
            customer_artists[customer_id].add(artist_id)
            artist_popularity[artist_id] += ntracks

        pairs = set()

        for artists in customer_artists.values():
            for a, b in itertools.combinations(sorted(artists), 2):
                pairs.add((a, b))

        for a, b in pairs:

            pop_a = artist_popularity[a]
            pop_b = artist_popularity[b]

            weight = pop_a + pop_b

            if pop_a > pop_b:
                self._graph.add_edge(self._idMap[a], self._idMap[b], weight=weight)
            elif pop_a < pop_b:
                self._graph.add_edge(self._idMap[b], self._idMap[a], weight=weight)
            else:
                self._graph.add_edge(self._idMap[a], self._idMap[b], weight=weight)
                self._graph.add_edge(self._idMap[b], self._idMap[a], weight=weight)

    def getBestArtist(self):
        bestArtist = None
        bestScore = float('-inf')  # Inizia col valore più basso possibile

        for v in self._graph.nodes():
            outWeight = 0
            for _, _, data in self._graph.out_edges(v, data=True):
                outWeight += data["weight"]

            inWeight = 0
            for _, _, data in self._graph.in_edges(v, data=True):
                inWeight += data["weight"]

            score = outWeight - inWeight

            # Prendi il MAX (anche se negativo)
            if score > bestScore:
                bestScore = score
                bestArtist = v

        if bestArtist is None:
            return None, 0

        return bestArtist.Name, bestScore

    def getTop5Edges(self):

        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )

        return edges[:5]
