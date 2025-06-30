from babel.core import Locale

import xml.etree.ElementTree as ET
import logging
import os


def add(key: str, value: str, files: dict[str, tuple[Locale, ET]]) -> None:
    for file_path, v in files.items():
        logging.debug(f'Adding "{key}" with value "{value}" to {file_path}')

        root = v[1].getroot()

        # Check if the string already exists
        for string in root.findall('string'):
            if string.get("name") == key:
                logging.info(f'{key} already exists in {file_path}')
                continue
        
        new_element = ET.Element('string', name=key)
        new_element.text = value
        root.append(new_element)

        logging.debug(f'Added {key} to {file_path}')
