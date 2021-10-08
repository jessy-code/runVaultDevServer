import argparse
import sys
from time import sleep

import Constant
from VaultDevServer import VaultDevServer, stop_vault_server
from envVarSetting import set_unix_environment_variables


def get_user_inputs():
    # Input variable definition
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Script which start or stop a vault dev server')
    parser.add_argument('mode', help='start to start a dev vault server. stop to stop it.', type=str)
    parser.add_argument('--unseal_key_path', help='File path where the unseal key will be stored', type=str)
    return parser.parse_args()


def main(argv):
    user_inputs = get_user_inputs()
    mode = user_inputs.mode
    unseal_key_path = user_inputs.unseal_key_path if user_inputs.unseal_key_path is not None else Constant.UNSEAL_PATH

    if mode == "start":
        vault_server_dev = VaultDevServer()
        if vault_server_dev.start_vault_server() == 0:
            # if vault server is running, set the environment
            file_creation = 0
            vault_addr = vault_server_dev.get_vault_addr()
            root_token_id = vault_server_dev.get_root_token_id()

            while (not vault_addr) or (not root_token_id):
                vault_addr = vault_server_dev.get_vault_addr()
                root_token_id = vault_server_dev.get_root_token_id()
                sleep(1)
                file_creation += 1
                if file_creation > 60:
                    print("Timeout error: impossible to get information on vault server. "
                          "Please check vault_server_status/vault_server_dev.log file to understand the issue")
                    return -1

            set_unix_environment_variables({"VAULT_ADDR": vault_addr,
                                            "VAULT_DEV_ROOT_TOKEN_ID": root_token_id})
            vault_server_dev.get_unseal_key(unseal_key_path)
            print("Vault server is on.")
            return 0

        else:
            print("Impossible to run vault development server. Please check " + Constant.OUTPUT_FILE_SERVER_RUN)
            return -1

    elif mode == "stop":
        stop_vault_server(unseal_key_path)

    else:
        print("Incorrect mode value. Run python3 testEnvVarSetting -h to check the available modes.")


if __name__ == '__main__':
    main(sys.argv[1:])
