class LinkIdentifier:
    def __init__(self, URI: str):
        self.URI = URI
        self.path = None
        self.parameters = None

    def validate_uri(self):
        scheme_split = self.URI.split(":")

        self.path = scheme_split[1].split("?")[0][2:]
        self.parameters = dict([parameter.split("=") for parameter in self.URI.split("?")[1].split("&")])

        if scheme_split[0] != "visma-identity":
            return False
        if not self.validate_parameters(self.path, self.parameters):
            return False
        return True

    def validate_parameters(self, path, parameters):
        valid_parameters = {"source": str}
        if path == "confirm":
            valid_parameters["paymentnumber"] = int
        if path == "sign":
            valid_parameters["documentid"] = str

        try:
            for key in valid_parameters:
                valid_parameters[key](parameters[key])
                del parameters[key]
        except:
            return False

        if len(parameters) != 0:
            return False
        return True
