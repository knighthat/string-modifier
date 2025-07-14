import re
import logging

from enums import Actions, FileType


REGEX_STRING_ID = r'^[a-z0-9](?:[a-z0-9_]*[a-z0-9])?$'

def request_string_id(request_message: str) -> str:
    print()
    print('ID must follow:')
    print('- Characters a-z and A-Z')
    print('- Numbers from 0-9')
    print('- Underscore(_) can be placed between chars but')
    print('  not at the start or the end of ID')
    print('- No special characters (except for underscore)')
    print('* You should keep ID in lowercase')

    string_id: str 
    while True:
        string_id = input('Specify string id: ').strip()

        if re.match(REGEX_STRING_ID, string_id):
            logging.debug(f'Input {string_id} matches {REGEX_STRING_ID}')
            break
        else:
            logging.error(f'{string_id} doesn\'t meet the requirements, please try again!')

    return string_id


def _get_type() -> FileType:
    file_type: FileType
    while True:
        try:
            print()
            print('Available types: strings, plurals')
            file_type_input: str = input('Please specify your file type: ').strip().upper()

            logging.debug(f'Input file type: {file_type_input}')

            file_type = FileType[file_type_input]
            break
        except KeyError:
            logging.error(f'Invalid file type {file_type_input}')
            logging.info('Please try again!')
            continue

    return file_type


def _get_action(file_type: FileType) -> Actions:
    action: Actions
    
    while True:
        try:
            print()
            if file_type == FileType.STRINGS:
                print('Available actions: add, remove, modify')
            else:
                print('Available actions: add, remove')
                
            action_input = input('Please specify your action: ').strip().upper()

            logging.debug(f'Input action: {action_input}')

            action = Actions[action_input]
            if action == Actions.MODIFY and file_type == FileType.PLURALS:
                raise KeyError('Modify is not allowed in plurals')

            break
        except KeyError:
            logging.error(f'Invalid action {action_input}')
            logging.info('Please try again!')
            continue

    return action


def select_action_and_file_type() -> tuple[Actions, FileType]:
    file_type: FileType = _get_type()
    action: Actions = _get_action(file_type)

    return (action, file_type)