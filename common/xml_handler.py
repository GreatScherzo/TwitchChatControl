import xml.etree.ElementTree as ET


class XMLHandler:
    def __init__(self, xml_path :str):
        self.root = ET.parse(xml_path).getroot()
        self.access_token = None
        self.refresh_token = None
        self.client_token = None

        for type_tag in self.root.findall('settings'):
            self.access_token = type_tag.find('access_token').text
            self.refresh_token = type_tag.find('refresh_token').text
            self.client_token = type_tag.find('client_id').text