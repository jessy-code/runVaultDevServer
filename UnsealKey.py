class UnsealKey:

    def __init__(self, path, key):
        self.path = path
        self.key = key

        self.__call__(self.path, self.key)

    def __call__(self, path, key):
        with open(path, 'w') as key_file:
            key_file.write(key)
