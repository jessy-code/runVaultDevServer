#!/usr/bin/env python3
import os
from getpass import getuser
from os import system
from os.path import isfile
import sys
import argparse


def get_bashrc_path():
    current_user = getuser()
    return '/home/' + current_user + '/.bashrc'


def get_bashrc_content():
    bashrc_content = ''
    with open(get_bashrc_path(), 'r') as file:
        bashrc_content = file.readlines()
    return bashrc_content


def set_unix_environment_variables(dictionary_vars):
    bashrc_content = get_bashrc_content()

    with open(get_bashrc_path(), 'a') as file:
        [file.write("export " + key + "=" + dictionary_vars[key] + "\n") for key in dictionary_vars.keys()
         if ("export " + key + "=") not in ''.join(bashrc_content)]

    if isfile('setting.sh'):
       os.system('rm setting.sh')

    with open('setting.sh', 'w') as file:
        file.write("#!/bin/bash\n")
        [file.write("export " + key + "=" + dictionary_vars[key] + "\n") for key in dictionary_vars.keys()]
    print("Run setting.sh script to take modification into account")


def unset_unix_environment_variable(dictionary_vars):
    bashrc_content = get_bashrc_content()
    forbidden_lines = ["export " + key + "=" for key in dictionary_vars.keys()]

    with open(get_bashrc_path() + '_current', 'w') as file:
        [file.write(line) for line in bashrc_content if line.split("=")[0] not in ''.join(forbidden_lines)]

    if not isfile('setting.sh'):
        os.system('rm setting.sh')

    with open('setting.sh', 'w') as file:
        file.write("#!/bin/bash\n")
        [file.write("unset " + key + "\n") for key in dictionary_vars.keys()]
    system('mv -f ' + get_bashrc_path() + '_current' + ' ' + get_bashrc_path())
    print("Run setting.sh script to take modification into account")


def get_user_inputs():
    # Input variable definition
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Script which set or unset environment variables')
    parser.add_argument('mode', help='set to add variable. unset to remove them', type=str)
    parser.add_argument('variable_list', help='list of variable (, separator)', type=str)
    parser.add_argument('--value_list', help='list of value (, separator)', type=str)
    return parser.parse_args()


def main(argv):
    user_inputs = get_user_inputs()
    mode = user_inputs.mode
    variable_dictionnary = dict(zip(user_inputs.variable_list.split(','), user_inputs.value_list.split(','))) \
        if user_inputs.value_list is not None \
        else dict(zip(user_inputs.variable_list.split(','), ['' for element in user_inputs.variable_list.split(',')]))
    if mode == "set":
        set_unix_environment_variables(variable_dictionnary)
    elif mode == "unset":
        unset_unix_environment_variable(variable_dictionnary)
    else:
        print("Incorrect mode value. Run python3 testEnvVarSetting -h to check the available modes.")


if __name__ == '__main__':
    main(sys.argv[1:])
