from babel.core import Locale

import xml.etree.ElementTree as ET
import logging
import os

from . import Rules


def _process_rules(locale: Locale, rules: Rules) -> dict[str, str]:
    plural_rules: set[str] = set(locale.plural_form.rules.keys())
    # Always append other to the final result
    # If language doesn't have plural rules, 
    # `always` is the default.
    plural_rules.add('other')
    
    return {k: getattr(rules, k) for k in plural_rules}


def add(key: str, rules: Rules, files: dict[str, tuple[Locale, ET]]) -> None:
    for file_path, locale, tree in ((k, v[0], v[1]) for k, v in files.items()):
        logging.debug(f'Adding plural "{key}" to {file_path}')

        root = tree.getroot()

        # Check if the string already exists
        for string in root.findall('string'):
            if string.get("name") == key:
                logging.info(f'{key} already exists in {file_path}')
                continue
        
        plurals_element: ET.Element = ET.Element('plurals', name=key)
        for quantity, value in _process_rules(locale, rules).items():
            item_comment = ET.Comment('')

            item_element: ET.Element = ET.Element('item', quantity=quantity)
            item_element.text = value


            plurals_element.append(item_element)

        root.append(plurals_element)

    logging.debug(f'Added plural "{key}" to {file_path}')
    