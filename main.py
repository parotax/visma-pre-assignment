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
