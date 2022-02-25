
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AeL4VXjka2yAxYxOidpeIrs0GVwgQmzlxzfwY7QUyvWWMBD44fnBYRNReUSD77UDbV1ut-T1DOM2zSff"
        self.client_secret = "EM05d9V6lqSIPMpm3ug0FUNvbUmSh2jHRix-2vkEMjXVhE4VP7D2fSdnPzUaxfNA9FGepUpnGfsR28lH"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)