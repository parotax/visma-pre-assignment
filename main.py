class LinkIdentifier:
    def __init__(self, URI: str):
        self.URI = URI

    def validate_uri(self):
        URI_parts = {}
        scheme_split = self.URI.split(":")

        URI_parts["scheme"] = scheme_split[0]
        URI_parts["path"] = scheme_split[1].split("?")[0][2:]
        URI_parts["parameters"] = dict([parameter.split("=") for parameter in self.URI.split("?")[1].split("&")])

        print("URI parts:", URI_parts)

        if URI_parts["scheme"] != "visma-identity":
            return False

        if not self.validate_parameters(URI_parts["path"], URI_parts["parameters"]):
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
