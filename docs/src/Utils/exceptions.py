class NoModelException(Exception):
    """
    Exception being raised if no model or experiment is found in MLflow.
    """
    def __init__(self, info):
        super().__init__(info)

class ParserError(Exception):
    """
    Exception being raised if there are syntactic errors in the parsed file.
    """
    def __init__(self, info):
        super().__init__(f"Check commands in config.yml: {info}")
