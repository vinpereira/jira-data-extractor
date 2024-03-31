import csv
from colorama import Fore

class Writer:
    def __init__(self, parser, output_file):
        self.parser = parser
        self.output_file = output_file

    def write_csv(self):
        print("Writing CSV file...")
        with open(self.output_file, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Link', 'Name'] + list(self.parser.status_mapping.keys()) + list(self.parser.attributes.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.parser.data:
                writer.writerow(row)

        print(f"Writing CSV file... {Fore.GREEN}done!\n")

        print(f"Results written to {self.output_file}")
