# Oracle plz don't change stuff I JUST got this working :(
# Oracle plz no sue me thank

# This script is designed to get all the CVE data from the Oracle CPUs and give it in CSV format - specifically the CVEs in the tables. nothing else.
# This script exists because Oracle doesn't provide a CSV of the CVEs listed in the CPUs

# Disclaimer: I have used selenium only once prior to this and I'm sure this is not the best way to do this.
# "AI" disclaimer - chatGPT was used as a tool in making this script, but this script is not "AI" generated.
# i.e. I wrote this script, and chatGPT fixed specific issues, made some good suggestions, and provided snippets that were used.
# Specific disclosures:
# the entire setup_driver function was generated - I was not originally using selenium until it was suggested by chatGPT
# restructuring of the extract_data function was assisted by chatGPT:
#### getting the exact classes/elements figured out was assisted by chatGPT
#### csv creation/formatting were adjusted by chatGPT after figuring out the classes/elements as mentioned above.
#### adding the sleep in there was suggested by chatGPT as webdriverwait didn't work for me for some reason.

# import some stuff we need and some stuff we probably don't need anymore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import csv, sys, getopt
from time import sleep

# selenium driver stuff
def setup_driver():
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver # Tu-tu-du-du Max Verstappen

# do all the actual work here
def extract_data(url, output_csv):
    # no more F1 references. I promise.
    driver = setup_driver()
    try:
        driver.get(url)
        
        # let it rest a bit otherwise stuff breaks 
        sleep(5)  # 5 seems good but you may need to increase this

        # get the divs with class 'otable otable-sticky otable-tech' which seems to be the tables we want
        cve_tables = driver.find_elements(By.CSS_SELECTOR, "div.otable.otable-sticky.otable-tech")
        cve_rows = []
        # get the data
        for cve_table in cve_tables:
            # get the table rows (within <tbody>)
            rows = cve_table.find_elements(By.CSS_SELECTOR, "table.otable-w2 tbody tr")
            for row in rows:
                try:
                    # check <th> element for "CVE-" - this should indicate we are in the right place
                    cve_id_cell = row.find_element(By.CSS_SELECTOR, "th.otable-col-sticky")
                    if cve_id_cell and cve_id_cell.text.startswith("CVE-"):
                        # get everything for the row since it starts with "CVE-" and that is what we want
                        cells = row.find_elements(By.TAG_NAME, "td")
                        row_data = [cve_id_cell.text.strip()] + [cell.text.strip() for cell in cells]
                        cve_rows.append(row_data)
                except Exception as e:
                    # Debug: This may or may not give you useful information (triggers for some stuff that we dont care about)
                    #print("There was an issue with a row:")
                    #print(row_data)
                    continue  # do not stop on error

        # formatting and create the file
        if cve_rows:
            with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["CVE", "Component", "Package/Privilege Required", "Protocol", "Remote Exploit", "Base Score", "Attack Vector", "Attack Complexity", "Privileges Required", "User Interaction", "Scope", "Confidentiality", "Integrity", "Availability", "Supported Versions", "Notes"])
                writer.writerows(cve_rows)
            print(f"CVE data saved to {output_csv}")
        else:
            print("CVE data couldn't be found - Oracle probably changed something so this script is busted :( ")
    # This shouldn't be hit unless stuff changed a lot
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit() # you are the world champion (ok NOW no more F1 references)

# get args and run the rest of everything      
def main(argv):
    # old hard coded info - leaving this for reference
    #url = "https://www.oracle.com/security-alerts/cpujan2025.html"
    #output_csv = "cpujan2025.csv"

    url = ''
    output_csv = ''
    
    #Debug - ignore this
    #print(len(argv))
    #for arg in argv:
    #    print(arg)

    # I should have just used argparse
    if len(argv) == 0:
        print("Error: must have arguments.")
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    elif len(argv) > 4:
        print("Error: too many arguments.")
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    elif 1 < len(argv) < 4:
        print("Error: argument seems to be missing.")
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    elif len(argv) == 1 and not (argv[0] == "-h") and not (argv[0] == "--help"):
        print("Error: single argument must be -h or --help.")
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    elif len(argv) == 4 and not (argv[0] == "-u") and not (argv[0] == "--url") and not (argv[0] == "-o") and not (argv[0] == "--outfile"):
        print(f"Error: {argv[0]} is invalid")
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    elif len(argv) == 4 and not (argv[2] == "-u") and not (argv[2] == "-o"):
        print(f"Error: {argv[2]} is invalid")
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv,"hu:o:",["help=","url=","outfile="])
    except getopt.GetoptError:
        print('CPUScrape.py -u <url> -o <outfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('CPUScrape.py -u <url> -o <outfile>')
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-o", "--outfile"):
            output_csv = arg
        else:
            print("how did you manage this?")
    # debug that I kept in cause it is nice to verify 
    print(f"checking {url}")
    print(f"saving to {output_csv}")
    # this runs all the stuff yay
    extract_data(url, output_csv)
    
# actual main
if __name__ == "__main__":
    # run the other main
    main(sys.argv[1:])
