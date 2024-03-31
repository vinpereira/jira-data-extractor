from datetime import datetime
from pytz import timezone
from collections import OrderedDict
from colorama import Fore

class Parser:
    def __init__(self, query, status_mapping, feature_flags, attributes):
        self.query = query
        self.status_mapping = status_mapping
        self.mask_link = feature_flags['MaskLink']
        self.mask_name = feature_flags['MaskName']
        self.attributes = attributes
        self.data = self.parse_data()

    def parse_data(self):
        print("Parsing Jira issues data...")
        data = []

        for issue in self.query.issues:
            row = {
                'ID': issue.key,
                'Link': '' if self.mask_link else issue.permalink(), 
                'Name': '' if self.mask_name else issue.fields.summary
            }

            for attr_key, attr_value in self.attributes.items():
                attr_obj = getattr(issue.fields, attr_value, None)
                if attr_obj:
                    if attr_value == 'parent':
                        row[attr_key] = attr_obj.key if hasattr(attr_obj, 'key') else ''
                    elif hasattr(attr_obj, 'name'):
                        row[attr_key] = attr_obj.name if hasattr(attr_obj, 'name') else ''
                    # elif attr_value == 'customfield_11608':
                    #     row[attr_key] = attr_obj[0].value
                    else:
                        row[attr_key] = attr_obj

            for history in issue.changelog.histories:
                for item in history.items:
                    if item.field == 'status':
                        for key, values in self.status_mapping.items():
                            if item.toString in values:
                                dt = datetime.strptime(history.created, '%y-%m-%dT%H:%M:%S.$f%z')
                                dt = dt.astimezone(timezone('UTC'))
                                current_date = dt.strftime('%Y-%m-%d')

                                # if key already exists in dict and current_date is newer
                                if key in row and row[key] < current_date:
                                    row[key] = current_date
                                # if key does not exists in dic, then add it
                                elif key not in row:
                                    row[key] = current_date
                                    
                            if issue.fields.status.name == 'Done':
                                dt = datetime.strptime(issue.fields.resolutiondate, '%Y-%m-%dT%H:%M:%S.%f%z')
                                dt = dt.astimezone(timezone('UTC'))
                                row['Done'] = dt.strftime('%Y-%m-%d')
                            
            row['To Do'] = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(timezone('UTC')).strftime('%Y-%m-%d')
            
            ordered_row = OrderedDict()
            for key in ['ID', 'Link', 'Name'] + list(self.status_mapping.keys()) + list(self.attributes.keys()):
                ordered_row[key] = row.get(key, '')

            date_columns = list(self.status_mapping.keys())
            
            for key in ordered_row:
                prev_date = None

                for col in date_columns:
                    current_date = ordered_row[key][col]

                    if prev_date is not None and current_date < prev_date:
                        ordered_row[key][col] = ''
                    
                    prev_date = current_date

            data.append(ordered_row)
        
        print(f"Parsing Jira issues data... {Fore.GREEN}done!\n")
        
        return data
