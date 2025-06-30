from babel.core import Locale

import xml.etree.ElementTree as ET
import logging
import os


def modify(key: str, new_value: str, is_forced: bool, files: dict[str, tuple[Locale, ET]]) -> None:
    default_text: str = ''
    # Set default_text to value of <string> with name matches key
    # in original `res/values/strings.xml`
    if not is_forced:
        for file_path, v in files.items():
            parent = os.path.dirname(file_path)
            parent = os.path.basename(parent)

            print(f'Parent: {parent}')

            if parent != 'values':
                continue

            root: ET.Element = v[1].getroot()
            for entry in root.findall('string'):
                if entry.get('name') == key:
                    default_text = entry.text

    modified_count: int = 0
    for file_path, v in files.items():
        logging.debug(f'Modifying "{key}" in {file_path}')

        root: ET.Element = v[1].getroot()
        
        is_key_found: bool = False
        for entry in root.findall('string'):
            if entry.get('name') != key:
                continue

            if is_forced or entry.text == default_text:
                logging.debug(f'Replacing {entry.text} with {new_value}')

                entry.text = new_value
                modified_count += 1


    logging.info(f'Modified {modified_count} files')
