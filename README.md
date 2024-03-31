## Jira Data Extractor

I used a lot the Actionable Agile extractor (https://github.com/ActionableAgile/jira-to-analytics) and since Jira had rollout its new _parent_ field -- replacing both _Parent Link_ and _Epic Link_ -- I noticed that AA extractor was not capturing the new field.

So, using such reason and my eagerness to comeback to coding, I decided to start this project. 

Like mentioned before, I used the AA extractor as my start point. Due to that, this project has a YAML file to config:
- Jira connection
- a query in JQL to search issues
- the workflow that holds a 1:1 or 1:many relationship
- attributes (jira fields and custom fields) to save in the CSV file
- options to mask issue summary (title) and link