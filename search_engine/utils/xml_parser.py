from typing import List
import xml.etree.ElementTree as ET

class XmlParser(object):
    def __init__(self, input_file: str) -> None:
        self.input_file = input_file
        webpage_elements = ET.parse(input_file).findall('webpage')
        self.webpages = {w.attrib['name']: w for w in webpage_elements}

    def get_links(self, url: str) -> List[str]:
        try:
            webpage = self.webpages[url]
            return [link.attrib['name'] for link in webpage.findall('link')]
        except KeyError:
            return []

    def get_content(self, url: str) -> List[str]:
        try:
            webpage = self.webpages[url]
            content = [word.strip(' ,.\n;:\'\"\t!@#$%^&*()_-=+[]?<>') for word in webpage.find('content').attrib['value'].split()]
            content = [word.lower() for word in content if word != '']
            return content
        except KeyError:
            return []
