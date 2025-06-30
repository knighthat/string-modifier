from babel.core import Locale, UnknownLocaleError
import xml.etree.ElementTree as ET

import os
import re
import logging


# Common Android config qualifiers to exclude
non_locale_qualifiers = [
    "night", "land", "port", "sw600dp", "hdpi", "mdpi",
    "xhdpi", "xxhdpi", "xxxhdpi", "v21", "v29", "v31",
    "ldrtl", "notnight", "anydpi", "nodpi"
]

def extract_tag(dirname: str) -> str | None:
    # Verify that 'root' actually a 'values' directory,
    # either ending with a language code or not.
    match = re.match(r"values(?:-(.+))?", dirname)
    if match:
        suffix = match.group(1)
        if not suffix:
            return 'default'

        # Skip if only contains known config qualifiers
        parts = suffix.split('-')
        if all(part in non_locale_qualifiers for part in parts):
            return None
        # Parse locale parts only
        locale_parts = [part for part in parts if part not in non_locale_qualifiers]
        if not locale_parts:
            return None
            
        # Normalize: underscores to dashes, b+en+US -> en-US
        tag = '-'.join(locale_parts)
        if tag.startswith("b+"):
            tag = tag[2:].replace('+', '-')
        else:
            region_match = re.match(r'^([a-z]{2})-r([A-Z]{2})$', tag)
            if region_match:
                tag = f'{region_match.group(1)}-{region_match.group(2)}'

        return tag
        
    return None


def load_files(res_path: str, filename: str) -> dict[str, tuple[Locale, ET]]:
    """
    Recursively load all `filename` files in 'res_path'.
    
    These files must be located in `values-*` directory (with the exception of
    default `values` directory).

    Args:
        res_path: Path to 'res' directory
        filename: Name of the file too look for in `values` directory.

    Returns:
        Dictionary of paths and tuple of values locale and their XML content as ET inside `values`.
    """
    logging.debug('Getting files...')

    files: dict[str, tuple[Locale, ET]] = {}

    for values_dir in os.listdir(res_path):
        # res/values-*/strings.xml or res/values-*/plurals.xml
        file_path = os.path.join(res_path, values_dir, filename)
        tree: ET
        locale: Locale

        tag = extract_tag(values_dir)
        if tag == 'default':
            logging.debug(f'{values_dir} is a default directory')
        elif tag:
            try:
                locale = Locale.parse(tag.replace('-', '_'))

                logging.debug(f'{values_dir} has tag {tag}')
            except UnknownLocaleError:
                logging.debug(f'{values_dir} is not a valid values dir')
                continue
        elif not tag:
            continue

        # Additional confirmation to prevent error
        if os.path.exists(file_path):
            tree = ET.parse(file_path)
        else:
            logging.debug(f'{filename} doesn\'t exist in {values_dir}, creating one...')

            root = ET.Element('resources')
            tree = ET.ElementTree(root)

        files[file_path] = (locale, tree)

    if not files:
        logging.info(f'Couldn\'t find any {filename}')
    else:
        logging.info(f'Found {len(files)}')
    logging.debug('Getting files completed!')

    return files