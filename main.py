class LinkIdentifier:
    def __init__(self, uri: str):
        self.__uri = uri
        self.__path = None
        self.__parameters = None

    def path(self):
        return self.__path

    def parameters(self):
        return self.__parameters

    def is_valid_uri(self):
        scheme, rest = self.__uri.split(':', 1)
        if scheme != "visma-identity":
            return False
        path, query_string = rest.split('?', 1)
        self.__path = path
        self.__parameters = dict(q.split('=') for q in query_string.split('&'))
        print(self.__parameters)
        if not self.is_valid_parameters():
            return False
        return True

    def is_valid_parameters(self):
        valid_parameters = {"source": str}
        if self.__path == "confirm":
            valid_parameters["paymentnumber"] = int
        if self.__path == "sign":
            valid_parameters["documentid"] = str

        try:
            for key, value in valid_parameters.items():
                value(self.__parameters[key])
                del self.__parameters[key]
        except ValueError:
            return False

        if len(self.__parameters) != 0:
            return False

        return True
