import xml.etree.ElementTree as ET


class XMLHandler:
    def __init__(self, xml_path :str):
        self.root = ET.parse(xml_path).getroot()
        self.access_token = None
        self.refresh_token = None
        self.client_token = None

        self.channel_name = None

        self.game_type = None
        self.game_window_title = None

        # Get authorization info
        for type_tag in self.root.findall('authorization'):
            self.access_token = type_tag.find('access_token').text
            self.refresh_token = type_tag.find('refresh_token').text
            self.client_token = type_tag.find('client_id').text

        # Get basic info
        for type_tag in self.root.findall('basic'):
            self.channel_name = type_tag.find('channel_name').text

        # Get game_controller settings
        for type_tag in self.root.findall('game_control_option'):
            self.game_type = type_tag.find('game_type').text
            self.game_window_title = type_tag.find('game_window_title').text

        # Assert that all required variables are not none
        assert self.access_token is not None
        assert self.refresh_token is not None
        assert self.client_token is not None