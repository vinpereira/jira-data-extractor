from extractor.connection import Connection
from extractor.query import Query
from extractor.parser import Parser
from extractor.writer import Writer
import argparse
import yaml
import time
from colorama import Fore, init
init(autoreset=True)

parser = argparse.ArgumentParser(description="A Jira Extrator tool that asks for input YAML file and CSV file for results")
parser.add_argument("-i", "--input", type=str, default="config.yaml", help="path to the YAML config file.")
parser.add_argument("-o", "--output", type=str, default="output.csv", help="path to the CSV file with the results.")

args = parser.parse_args()

start_time = time.time()

print("Jira Extractor configuring...\n")

with open(args.input, 'r') as file:
    config = yaml.safe_load(file)

connection = Connection(config['Connection'])
query = Query(connection, config['Criteria']['Query'])
parser = Parser(query, config['Workflow'], config['Feature Flags'], config['Attributes'])
writer = Writer(parser, args.output)

writer.write_csv()

end_time = time.time()

print(f"{Fore.GREEN}Jira Extractor completed in {end_time - start_time} seconds!")