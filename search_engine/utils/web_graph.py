from typing import List

class WebVertex(object):
    def __init__(self, url: str) -> None:
        self.url = url
        self.links = []
        self.visited = False
        self.rank = 0
    
    def __repr__(self) -> str:
        return f"{self.url}   {self.visited}    {self.rank}"

    def add_edge(self, v: str) -> bool:
        if v not in self.links:
            self.links.append(v)
            return True
        return False
    
    def get_neighbours(self) -> List[str]:
        return self.links

    def contains_edge(self, v: str) -> bool:
        return v in self.links


class WebGraph(object):
    def __init__(self) -> None:
        self.vertex_dict = dict()
    
    def __repr__(self) -> str:
        return '\n'.join([str(v) for v in self.vertex_dict.values()])
    
    def add_vertex(self, s: str) -> bool:
        if s not in self.vertex_dict:
            self.vertex_dict[s] = WebVertex(s)
            return True
        return False

    def add_edge(self, s: str, t: str) -> bool:
        """Add an edge from vertex s to vertex t.u

        Args:
            s (str): URL of vertex 1
            t (str): URL of vertex 2

        Returns:
            bool: True if an edge was successfully added, False otherwise
        """
        if s in self.vertex_dict and t in self.vertex_dict:
            return self.vertex_dict[s].add_edge(t)
        return False

    def get_neighbours(self, url: str) -> List[str]:
        try:
            return self.vertex_dict[url].get_neighbours()
        except KeyError:
            return []
    
    def get_vertices(self) -> List:
        return list(self.vertex_dict.keys())

    def get_edges_into(self, url: str) -> List[str]:
        """Returns the list of vertices that have links into the given vertex

        Args:
            url (str): URL of the given vertex

        Returns:
            List: List of URLs of vertices that link to the given vertex
        """

        links_into = [k for k, v in self.vertex_dict.items() if v.contains_edge(url)]

        return links_into
    
    def get_out_degree(self, url: str) -> int:
        try:
            return len(self.vertex_dict[url].get_neighbours())
        except KeyError:
            return 0

    def get_page_rank(self, url: str) -> float:
        try:
            return self.vertex_dict[url].rank
        except KeyError:
            return 0.0
    
    def set_page_rank(self, url: str, page_rank: float) -> None:
        try:
            self.vertex_dict[url].rank = page_rank
        except KeyError:
            return
    
    def get_visited(self, url: str) -> bool:
        try:
            return self.vertex_dict[url].visited
        except KeyError:
            return False

    def set_visited(self, url: str, visited: bool) -> bool:
        try:
            self.vertex_dict[url].visited = visited
            return True
        except KeyError:
            return False
