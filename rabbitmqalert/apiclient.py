import urllib.request
import urllib.error
import json


class ApiClient:

    def __init__(self, log, arguments):
        self.log = log
        self.arguments = arguments

    def get_queue(self):
        uri = "/api/queues/{}/{}".format(self.arguments["server_vhost"], self.arguments["server_queue"])
        data = self.send_request(uri)
        return data

    def get_queues(self):
        uri = "/api/queues?page=1&page_size=300"
        data = self.send_request(uri)
        if data is None:
            self.log.error("No queues discovered (request failed).")
            return []

        queues = [queue.get("name") for queue in data.get("items", [])]

        if queues:
            self.log.info(f"Queues discovered: {', '.join(queues)}")
        else:
            self.log.error("No queues discovered.")

        return queues

    def get_connections(self):
        uri = "/api/connections"
        return self.send_request(uri)

    def get_consumers(self):
        uri = "/api/consumers"
        return self.send_request(uri)

    def get_nodes(self):
        uri = "/api/nodes"
        return self.send_request(uri)

    def send_request(self, uri):
        url = f"{self.arguments['server_scheme']}://{self.arguments['server_host']}:{self.arguments['server_port']}{uri}"
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, self.arguments["server_username"], self.arguments["server_password"])
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)

        try:
            request = opener.open(url)
            response = request.read()
            request.close()

            return json.loads(response.decode('utf-8'))
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            self.log.error(f"Error while consuming the API endpoint \"{url}\": {e}")
            return None
