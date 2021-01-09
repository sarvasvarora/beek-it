from typing import List
import xml.etree.ElementTree as ET


class XmlParser(object):
    def __init__(self, input_file: str) -> None:
        """Initialize the XML parser

        Args:
            input_file (str): Path to the XML file to be parsed
        """
        self.input_file = input_file
        webpage_elements = ET.parse(input_file).findall('webpage')
        self.webpages = {w.attrib['name']: w for w in webpage_elements}

    def get_links(self, url: str) -> List[str]:
        """Get the links in the given webpage.

        Args:
            url (str): URL of the webpage

        Returns:
            List[str]: List of URLs in the given webpage
        """
        try:
            webpage = self.webpages[url]
            return [link.attrib['name'] for link in webpage.findall('link')]
        except KeyError:
            return []

    def get_content(self, url: str) -> List[str]:
        """Get the content of the given webpage.

        Args:
            url (str): URL of the webpage

        Returns:
            List[str]: List of words (in lowercase, punctuation removed) in the given webpage
        """
        try:
            webpage = self.webpages[url]
            content = [word.strip(' ,.\n;:\'\"\t!@#$%^&*()_-=+[]?<>') for word in webpage.find('content').attrib['value'].split()]
            content = [word.lower() for word in content if word != '']
            return content
        except KeyError:
            return []
