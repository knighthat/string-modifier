import re
import logging


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