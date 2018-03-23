import requests
import httpimport
import time
import json
import traceback

BASE_URL = 'http://127.0.0.1:5002'
httpimport.INSECURE = True

def run_command(data_dict):
    print(data_dict)
    httpimport.add_remote_repo(data_dict['import_list'], data_dict['import_base_url'])
    main = httpimport.load(data_dict['main'], data_dict['main_base_url'])
    main.main()
    print('imported')


def check_commands():
    commands = json.loads(requests.get('{}/commands'.format(BASE_URL)).text)
    for command in commands:
        try:
            run_command(command)
        except Exception as e:
            print(e)
            print(traceback.format_exc())


def main():
    while True:
        try:
            check_commands()
            time.sleep(10)
        except:
            print('Oh no something went wrong.')


if __name__ == '__main__':
    main()
