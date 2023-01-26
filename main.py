class LinkIdentifier:
    """
    A class that validates a URI and extracts its path and parameters.
    """
    def __init__(self, uri: str):
        """
        Initialize the class with the URI.
        """
        self.__uri = uri
        self.__path = None
        self.__parameters = None
        self.__valid_paths = ["login", "sign", "confirm"]

    def path(self):
        """
        Return the path of the URI.
        """
        return self.__path

    def parameters(self):
        """
        Return the parameters of the URI.
        """
        return self.__parameters

    def is_valid_uri(self):
        """
        Validate the URI.
        """
        # Split the URI into scheme and rest
        scheme, rest = self.__uri.split(":", 1)

        # Check if the scheme is "visma-identity"
        if scheme != "visma-identity":
            return False

        # Split the rest into path and query string
        path, query_string = rest.split("?", 1)
        self.__path = path[2:]
        self.__parameters = dict(q.split("=") for q in query_string.split("&"))

        # Check if the path is valid
        if self.__path not in self.__valid_paths:
            return False
        # Check if the parameters are valid
        if not self.is_valid_parameters():
            return False
        return True

    def is_valid_parameters(self):
        """
        Validate the parameters of the URI.
        """
        # Define the required parameters and their types
        valid_parameters = {"source": str}
        if self.__path == "confirm":
            valid_parameters["paymentnumber"] = int
        elif self.__path == "sign":
            valid_parameters["documentid"] = str

        # Create a copy of the parameters to avoid modifying the original
        parameters = self.__parameters.copy()

        # Check if all required parameters are present and of the correct type
        for key, value in valid_parameters.items():
            try:
                value(parameters[key])
                del parameters[key]
            except (ValueError, KeyError):
                return False

        # Check if there are any additional parameters present
        if parameters:
            return False
        return True

class LinkIdentifierClient:
    """
    A client class for interacting with the LinkIdentifier class.
    """
    def __init__(self, uri: str):
        """
        Initialize the client with a URI string.
        """
        self.__link_identifier = LinkIdentifier(uri)

    def check_validity(self):
        """
        Check if the URI is valid.
        """
        return self.__link_identifier.is_valid_uri()

    def get_parameters(self):
        """
        Get the parameters of the URI.
        """
        if self.check_validity():
            return self.__link_identifier.parameters()
        raise ValueError("Invalid URI")

    def get_path(self):
        """
        Get the path of the URI.
        """
        if self.check_validity():
            return self.__link_identifier.path()
        raise ValueError("Invalid URI")

# Test code
URI = "visma-identity://sign?source=vismasign&documentid=105ab44"
client = LinkIdentifierClient(URI)
if client.check_validity():
    print(client.get_path())
    print(client.get_parameters())
else:
    raise ValueError("Invalid URI")
