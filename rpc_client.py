import requests

class OdooRPCClient:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None

    def _call(self, service, method, args):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args
            },
            "id": 1
        }

        response = requests.post(self.url, json=payload).json()

        if "error" in response:
            raise Exception(response["error"])

        return response["result"]

    def authenticate(self):
        self.uid = self._call(
            "common",
            "authenticate",
            [self.db, self.username, self.password, {}]
        )
        if not self.uid:
            raise Exception("Authentication failed")
        return self.uid

    def execute(self, model, method, *args, **kwargs):
        return self._call(
            "object",
            "execute_kw",
            [
                self.db,
                self.uid,
                self.password,
                model,
                method,
                list(args),  # <-- positional arguments
                kwargs  # <-- this gets sent as another positional argument
            ]
        )
