#!/bin/python

from babel.core import Locale

import os
import re
import logging
import xml.etree.ElementTree as ET
import sys

from file_loader import load_files
from enums import Actions, FileType
from strings import add as strings_add, remove as strings_remove, modify as strings_modify
from plurals import Rules, add as plurals_add, remove as plurals_remove


def select_action_and_file_type() -> tuple[Actions, FileType]:
    while True:
        try:
            print()
            print('Available actions: add, remove, modify')
            action_input: str = input('Please specify your action: ').strip().upper()

            logging.debug(f'Input action: {action_input}')

            action: Actions = Actions[action_input]

            break
        except KeyError:
            logging.error(f'Invalid action {action_input}')
            logging.info('Please try again!')
            continue

    while True:
        try:
            print()
            print('Available types: strings, plurals')
            file_type_input: str = input('Please specify your file type: ').strip().upper()

            logging.debug(f'Input file type: {file_type_input}')

            file_type: FileType = FileType[file_type_input]
            break
        except KeyError:
            logging.error(f'Invalid file type {file_type_input}')
            logging.info('Please try again!')
            continue

    return (action, file_type)


def write_to_files(files: dict[str, tuple[Locale, ET]]):
    def _write(file_path: str, tree: ET):
        root = tree.getroot()

        # Fix indentation
        ET.indent(root, space="    ")

        with open(file_path, 'wb') as file:

            tree = ET.ElementTree(root)
            tree.write(file, encoding="utf-8", xml_declaration=True)

            # Append new line to the end of strings.xml file
            file.write(b'\n')

        logging.info(f'Saved changes to {file_path}')
    
    for file_path, tree in ((k, v[1]) for k, v in files.items()):
        _write(file_path, tree)


# TODO: Add support for args (flags)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Contains localized sentences
    strings_files: dict[str, tuple[Locale, ET]] = {}
    # Contains localized word (single and plural forms)
    plurals_files: dict[str, tuple[Locale, ET]] = {}

    while True:
        action, file_type = select_action_and_file_type()
        logging.debug(f'Action: {action}')
        logging.debug(f'File type: {file_type}')

        # Only load files when selected and files aren't loaded 
        # This is here to prevent subsequent run from overriding
        # previous changes
        if file_type == FileType.STRINGS and not strings_files:
            strings_files = load_files( sys.argv[1], 'strings.xml')
        if file_type == FileType.PLURALS and not plurals_files:
            plurals_files = load_files( sys.argv[1], 'plurals.xml')

        if not strings_files and not plurals_files:
            logging.info('There\'s no file to process! Exiting...')
            break

        string_id_regex = r'^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$'
        if action == Actions.ADD:
            print()
            print('ID must follow:')
            print('- Characters a-z and A-Z')
            print('- Numbers from 0-9')
            print('- Underscore(_) can be placed between chars but')
            print('  not at the start or the end of ID')
            print('- No special characters (except for underscore)')
            print('* You should keep ID in lowercase')

            while True:
                string_id: str = input('Specify string id: ').strip()

                if re.match(string_id_regex, string_id):
                    logging.debug(f'Input {string_id} matches {string_id_regex}')
                    break
                else:
                    logging.error(f'{string_id} doesn\'t meet the requirements, please try again!')

            if file_type == FileType.STRINGS:
                string_value: str = input(f'Enter value of "{string_id}": ').strip()

                strings_add(string_id, string_value, strings_files)
            else:
                general_value: str = input(f'Enter default value of "{string_id}": ').strip()
                rules: Rules = Rules(general_value)

                plurals_add(string_id, rules, plurals_files)


        if action == Actions.REMOVE:
            print()
            print('ID must follow:')
            print('- Characters a-z and A-Z')
            print('- Numbers from 0-9')
            print('- Underscore(_) can be placed between chars but')
            print('  not at the start or the end of ID')
            print('- No special characters (except for underscore)')
            print('* You should keep ID in lowercase')

            while True:
                string_id: str = input('Specify string id to remove: ').strip()
                
                if re.match(string_id_regex, string_id):
                    logging.debug(f'Input {string_id} matches {string_id_regex}')
                    break
                else:
                    logging.error(f'{string_id} doesn\'t meet the requirements, please try again!')

            if file_type == FileType.STRINGS:
                strings_remove(string_id, strings_files)
            else:
                plurals_remove(string_id, plurals_files)

        if action == Actions.MODIFY:
            print()
            print('ID must follow:')
            print('- Characters a-z and A-Z')
            print('- Numbers from 0-9')
            print('- Underscore(_) can be placed between chars but')
            print('  not at the start or the end of ID')
            print('- No special characters (except for underscore)')
            print('* You should keep ID in lowercase')

            while True:
                string_id: str = input('Specify string id to modify: ').strip()
                
                if re.match(string_id_regex, string_id):
                    logging.debug(f'Input {string_id} matches {string_id_regex}')
                    break
                else:
                    logging.error(f'{string_id} doesn\'t meet the requirements, please try again!')

            string_new_value: str = input(f'Enter new value for "{string_id}": ').strip()
            
            if file_type == FileType.STRINGS:
                strings_modify(string_id, string_new_value, True, strings_files)
                
        print()
        print('Do you wish to continue?')
        print('\'Y\' or \'Yes\' brings to back to step 1 while keeping your changes')
        continue_choice: str = input('(y/N): ').strip().capitalize()
        if continue_choice != "Y" and continue_choice != "Yes":
            if strings_files:
                write_to_files(strings_files)
            if plurals_files:
                write_to_files(plurals_files)

            logging.info('Closing app...')
            break






