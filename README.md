# OracleCPUScraper
Python scraper that grabs the Oracle CPU CVEs and puts em in a csv

# Info
Oracle plz don't change stuff I JUST got this working :(
Oracle plz no sue me thank

This script is designed to get all the CVE data from the Oracle CPUs and give it in CSV format
This script exists cause Oracle hates CSV files apparently :P plz just give us a CSV already

# Disclaimer: this is a hacky workaround - use at your own risk
## "AI" disclaimer - This script is not "AI" generated, but I did use chatGPT as a tool
i.e. I wrote this script, and chatGPT fixed specific issues, made some good suggestions, and provided snippets that were used.

## Specific disclosures:
* the entire setup_driver function was generated - I was not originally using selenium until it was suggested by chatGPT
* restructuring of the extract_data function was assisted by chatGPT:
  * getting the exact classes/elements figured out was assisted by chatGPT
  * csv creation/formatting were adjusted by chatGPT after figuring out the classes/elements as mentioned above.
  * adding the sleep in there was suggested by chatGPT as webdriverwait didn't work for me for some reason.
