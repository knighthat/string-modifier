from babel.core import Locale

import xml.etree.ElementTree as ET
import logging
import os


def remove(key: str, files: dict[str, tuple[Locale, ET]]) -> None:
    for file_path, v in files.items():
        logging.debug(f'Removing "{key}" from {file_path}')

        root: ET.Element = v[1].getroot()

        is_key_found: bool = False
        for entry in root.findall('string'):
            if entry.get('name') == key:
                root.remove(entry)
                is_key_found = True

        if not is_key_found:
            logging.info(f'{key} doesn\'t exist in {file_path}')