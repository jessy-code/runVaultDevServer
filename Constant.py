OUTPUT_FILE_SERVER_RUN = 'vault_server_status/vault_server_dev.log'
OUTPUT_FOLDER = 'vault_server_status/'
UNSEAL_PATH = OUTPUT_FOLDER + 'unseal.key'
RUN_SERVER_DEV = 'vault server -dev > ' + OUTPUT_FILE_SERVER_RUN + ' &'
