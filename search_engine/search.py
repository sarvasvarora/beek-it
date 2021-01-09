from typing import List
import re
from collections import defaultdict
from search_engine.utils.xml_parser import XmlParser
from search_engine.utils.web_graph import WebGraph


class SearchEngine(object):
    def __init__(self, filename: str) -> None:
        """Initialize the search engine object.

        Args:
            filename (str): Path to the XML database proxy.
        """
        self.word_index = defaultdict(list)
        self.internet = WebGraph()
        self.parser = XmlParser(filename)

    def __repr__(self) -> str:
        return self.internet.__repr__()

    def add_word_to_index(self, word: str, url: str) -> None:
        """Add a word to the word-index of the search engine.

        Args:
            word (str): Word to be added
            url (str): URL of the webpage
        """ 
        if url not in self.word_index[word]:
            self.word_index[word].append(url)

    def crawl_and_index(self, url: str) -> None:
        """Crawl and index the web, starting from the given URL.

        Args:
            url (str): URL of the webpage to start indexing from
        """
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
            self.add_word_to_index(word, url)

        # Crawl the web by visiting the links pointed to by the current URL
        links = self.parser.get_links(url)
        for link in links:
            self.internet.add_vertex(link)
            self.internet.add_edge(url, link)
            self.crawl_and_index(link)

    def _compute_ranks(self, vertices: List[str]) -> List[float]:
        """Complete one iteration of ranking webpages.

        Args:
            vertices (List[str]): List of webpages to rank

        Returns:
            List[float]: List of ranks of respective webpages
        """
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
        """Assign page ranks to the crawled webpages.

        Args:
            EPSILON (float): Epsilon value to control the convergence
        """
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

    def query(self, query: str, phrase_query: bool = False) -> List[str]:
        """Query the search engine.

        Args:
            query (str): Query phrase or keyword
            phrase_query (bool, optional): Whether exact phrase matching should be done. Defaults to False.

        Returns:
            List[str]: List of webpages, arranged in descending order of their page ranks
        """
        words = [word.strip(' ,.\n;:\'\"\t!@#$%^&*()_-=+[]?<>').lower() for word in query.split()]
        words = [word for word in words if word != '']
        urls = self.word_index[words[0]] # Initialize urls 

        if phrase_query is False:
            for word in words:
                tmp_urls = self.word_index[word]
                urls = list(set(urls + tmp_urls)) # Take union
        else:
            for word in words:
                tmp_urls = self.word_index[word]
                urls = list(filter((lambda x: x in tmp_urls), urls)) # Take intersection

                # break if at any point the intersection becomes empty. Reduces unnecessary computation
                if urls == []: 
                    break
            
            phrase = ' '.join(words)

            for url in urls:
                content = ' '.join(self.parser.get_content(url))
                if re.findall(phrase, content) == []:
                    urls.remove(url)

        ranks = [self.internet.get_page_rank(url) for url in urls]
        urls_with_rank = list(zip(urls, ranks))

        # Sort wrt to ranks (2nd element of tuples) and arrange in descending order
        urls_with_rank.sort(key=lambda x: x[1], reverse=True)
        return [e[0] for e in urls_with_rank]