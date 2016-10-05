# JIRA Scripts
A collection of utility scripts for managing JIRA entities (projects, issues, components, etc). This repository shall contain standalone scripts (python, bash scripts), [ScriptRunner / Groovy scripts](https://scriptrunner.adaptavist.com/latest/index.html) and [Bean Shell scripts](https://innovalog.atlassian.net/wiki/display/JMCF/JIRA+Misc+Custom+Fields) used in Misc Custom Fields plugin.

## Installation and Usage
Standalone scripts should only require basic `bash` and `python`. Plugin scripts should be stored on a separate folders and will have its own `README` file containing installation and usage instructions

## Contents 
- `bulk-delete-components.py`.

   Deletes all components in a JIRA project based on the passed project key.
   ```
   ./bulk-delete-components.py -k <project_key> -u <jira_username>
   ```

- `bulk-import-components.py`.

   Reads a csv file with a list of components and import them in a JIRA project based on the passed project key.
   ```
   ./bulk-import-components.py -k <project_key> -u <jira_username> <csv_file>
   ```
   Note: the csv file must contain a single component per row
    
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`. Make sure to update this `README` file with the description of the new script(s)
3. Commit your changes: `git commit -am 'New scripts'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

