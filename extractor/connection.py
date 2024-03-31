from jira import JIRA
from colorama import Fore

class Connection:
    def __init__(self, connection_config):
        self.connection_config = connection_config
        self.jira_connection = self.get_jira_connection()

    def get_jira_connection(self):
        username = self.connection_config['Username']
        api_token = self.connection_config['Password']
        domain = self.connection_config['Domain']

        print("Authenticating...")
        jira = JIRA(basic_auth=(username, api_token), options={'server': domain})
        print(f"{Fore.GREEN}Authentication successful.\n")
        return jira
