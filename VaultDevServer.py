import os
from os.path import isdir
from subprocess import check_output, CalledProcessError
from re import search

import Constant
from UnsealKey import UnsealKey
from envVarSetting import unset_unix_environment_variable


class VaultDevServer:

    def __init__(self):
        self.VAULT_ADDR = ''
        self.VAULT_DEV_ROOT_TOKEN_ID = ''
        self.unseal_key = ''
        self.server_status = False

    def start_vault_server(self):
        if isdir(Constant.OUTPUT_FOLDER):
            os.system('rm -r ' + Constant.OUTPUT_FOLDER)
        self.server_status = os.system("mkdir " + Constant.OUTPUT_FOLDER)
        self.server_status = os.system(Constant.RUN_SERVER_DEV)
        if self.server_status > 0:
            print('Impossible to run the Vault dev server. Please check the ' + Constant.OUTPUT_FILE_SERVER_RUN +
                  ' file to have more information')
        return self.server_status

    def get_vault_addr(self):
        try:
            with open(Constant.OUTPUT_FILE_SERVER_RUN, 'r') as file:
                self.VAULT_ADDR = [line.split('=')[1][1:-2] for line in file.readlines() if search('VAULT_ADDR=', line)
                                   is not None][0]

        except (FileNotFoundError, IndexError):
            return ""

        return self.VAULT_ADDR

    def get_root_token_id(self):
        try:
            with open(Constant.OUTPUT_FILE_SERVER_RUN, 'r') as file:
                self.VAULT_DEV_ROOT_TOKEN_ID = [line.split(':')[1][1:-1] for line in file.readlines()
                                                if search('Root Token: ', line) is not None][0]
        except (FileNotFoundError, IndexError):
            return ""
        return self.VAULT_DEV_ROOT_TOKEN_ID

    def get_unseal_key(self, file_path=Constant.UNSEAL_PATH):
        with open(Constant.OUTPUT_FILE_SERVER_RUN, 'r') as file:
            unseal_key = [line.split(':')[1][1:-1] for line in file.readlines()
                          if search('Unseal Key: ', line) is not None][0]

        self.unseal_key = UnsealKey(file_path, unseal_key)
        return self.unseal_key


def stop_vault_server(unseal_path=Constant.UNSEAL_PATH):
    try:
        os.system('ps | grep vault > test_vault.txt')
        vault_process_id = search('[0-9]* p', str(check_output('ps | grep vault', shell=True))).group().split(' ')[0]
        os.system('kill ' + vault_process_id)
        unset_unix_environment_variable({"VAULT_ADDR": "",
                                     "VAULT_DEV_ROOT_TOKEN_ID": ""})
        os.system('rm -f ' + unseal_path)
    except CalledProcessError:
        print("No vault server running")
        pass
