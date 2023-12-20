# mint2simplifi
Takes a bulk export CSV of all Mint transactions and breaks it into individual CSVs for each account for uploading into Simplifi by Quicken.

# How to use
1. Clone the repo locally
2. Run `python start.py` in your terminal in the directory where the script is located
3. Enter the file path for where your Mint export .csv file is located

It should output one CSV per Account in Mint in a separate "Covnerted CSVs" folder in the same folder as the Mint export. It will also generate a log file detailing what it did, the number of transactions per file and oldest recorded entry date in each, as well as logging any errors.
