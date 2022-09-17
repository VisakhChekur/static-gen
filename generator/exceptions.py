class NoMetadata(Exception):
    pass


class InvalidMetadataSyntax(Exception):
    pass


class ConfigNotFound(Exception):
    pass


class InvalidConfig(Exception):
    def __init__(self, error: str):

        super().__init__()
        self.error: str = error
