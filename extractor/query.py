from colorama import Fore

class Query:
    def __init__(self, connection, query):
        self.jira = connection.jira_connection
        self.query = query
        self.issues = self.get_issues()

    def get_issues(self):
        print("Getting Jira issues...")
        issues = self.jira.search_issues(self.query, expand='changelog', maxResults=False)
        print(f"Getting Jira issues... {Fore.GREEN}done!\n")

        return issues
