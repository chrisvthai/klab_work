import pandas as pd
from bs4 import BeautifulSoup
import os
from os import listdir
from os.path import isfile, join
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def get_dali_query(prot: str):
    binary = FirefoxBinary('/home/ct647/firefox/firefox')
    options = Options()
    options.headless = True

    web_driver = webdriver.Firefox(options=options, firefox_binary=binary)
    url = 'http://ekhidna2.biocenter.helsinki.fi/dali/'
    web_driver.get(url)

    # Formulate and send query
    tab = web_driver.find_element_by_id('ui-id-3')
    tab.click()
    form = web_driver.find_element_by_id('taxonomy')
    form.send_keys(prot)
    submit_button = web_driver.find_element_by_name('submit')
    submit_button.click()

    # Wait until job finishes
    def wait_for_results():
        try:
            web_driver.find_element_by_link_text('Download matches against PDB90')
            return False
        except:
            return True

    hrs = 24
    timeout = time.time() + 60*60*hrs
    while(wait_for_results()):
        if time.time() > timeout:
            print("Query for {} timed out".format(prot))
            return []
        time.sleep(10)
        pass

    link = web_driver.find_element_by_link_text('Download matches against PDB90')
    link.click()

    query_text = web_driver.find_element_by_tag_name('pre').get_attribute('innerHTML')

    # Parse the whole DALI query
    result_table = query_text.split('#')[3]
    rows = result_table.split('\n')
    rows.pop(0)
    rows[0]

    result_set = []
    for r in rows:
        if r:
            result_set.append(r.strip().split()[1])

    web_driver.quit()
    return result_set

number = sys.argv[1]
path = "./neighbors/neighbors_{}.txt".format(number)
print("Using path: {}".format(path))

with open(path, 'r') as f:
    proteins = f.readlines()
    proteins_revised = [ p[0:4] + p[5] for p in proteins  ]
    
    for p in proteins_revised:
        results = get_dali_query(p)

        write_path = './dali_dataset_neighbors/' + p + '.txt'

        # Write out new data
        outdir = './dali_dataset_neighbors/'
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        with open(write_path, 'w') as f_write:
            p_reformatted = p[:4].lower() + '-' + p[4]
            f_write.write(p_reformatted + '\n')
            f_write.writelines(m + '\n' for m in results)

        if results:
            print('Got result set for {}'.format(p))
        del results[:]



 
