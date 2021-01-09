from typing import List
from collections import defaultdict
from search_engine.utils.xml_parser import XmlParser
from search_engine.utils.web_graph import WebGraph


class SearchEngine(object):
    def __init__(self, filename: str) -> None:
        self.word_index = defaultdict(list)
        self.internet = WebGraph()
        self.parser = XmlParser(filename)

    def __repr__(self) -> str:
        return self.internet.__repr__()

    def add_word_to_index(self, word: str, url: str) -> None:
        if url not in self.word_index[word]:
            self.word_index[word].append(url)

    def crawl_and_index(self, url: str) -> None:
        # If the vertex with the given URL already exists AND has already been
        # visited
        if not self.internet.add_vertex(url) and self.internet.get_visited(url):
            return

        # If it didn't exist, it would've been added now
        # Set it to visited, and do further stuff
        self.internet.set_visited(url, True)

        # Index the current URL
        words = self.parser.get_content(url)
        for word in words:
            self.add_word_to_index(word.lower(), url)

        # Crawl the web by visiting the links pointed to by the current URL
        links = self.parser.get_links(url)
        for link in links:
            self.internet.add_vertex(link)
            self.internet.add_edge(url, link)
            self.crawl_and_index(link)

    def _compute_ranks(self, vertices: List[str]) -> List[float]:
        DAMPING_FACTOR = 0.5

        new_prV = [self.internet.get_page_rank(vertex) for vertex in vertices]

        for i, v in enumerate(vertices):
            W = self.internet.get_edges_into(v)
            prW_outW = []

            for w in W:
                j = vertices.index(w)
                prW = new_prV[j]
                outW = self.internet.get_out_degree(vertices[j])
                prW_outW.append(prW / outW)
            
            _sum = sum(prW_outW)
            rank = (1 - DAMPING_FACTOR) + (DAMPING_FACTOR * _sum)
            new_prV[i] = rank

        return new_prV

    def assign_page_ranks(self, EPSILON: float) -> None:
        prV = [1.0 for i in range(0, len(self.internet.get_vertices()))]

        while True:
            new_prV = self._compute_ranks(self.internet.get_vertices())
            converged = True

            for i in range(0, len(prV)):
                if abs(prV[i] - new_prV[i] > EPSILON):
                    converged = False
                    break
            
            if converged:
                break

            for i in range(0, len(prV)):
                prV[i] = new_prV[i]
                self.internet.set_page_rank(self.internet.get_vertices()[i], new_prV[i])

    def get_results(self, query: str) -> List[str]:
        urls = self.word_index[query.lower()]
        ranks = [self.internet.get_page_rank(url) for url in urls]
        urls_with_rank = list(zip(urls, ranks))

        # Sort wrt to ranks (2nd element of tuples) and arrange in descending order
        urls_with_rank.sort(key=lambda x: x[1], reverse=True)
        return [e[0] for e in urls_with_rank]
