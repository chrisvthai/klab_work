import pandas as pd
from bs4 import BeautifulSoup
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def get_dali_query(prot: str):
    web_driver = webdriver.Firefox()
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
    
    timeout = time.time() + 60*60*24 # 60 s - 60 min - 24 hrs
    while(wait_for_results()):
        if time.time() > timeout:
            print("Query for {} timed out".format(prot))
            return []
        time.sleep(1)
        
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

pa_proteins = {
    'C03': ['1L1NA', '1HAVA', '1CQQA', '2J92A', '2ZU3A', '2HRVA'],
    'C04': ['1LVMA'],
    'C37': ['1WQSA'],
    'S01': ['2GMTB', '1IAUA', '1A0LA', '2PSYA', '2OQ5A', '1OP0A', '2F91B', '1FI8A',
            '1BRAA', '1SGTA', '1TRYA', '2W5EA', '1DPOA', 
            '1HYLA', '1AZZA', '1A0JA',
            '1TRNA', '1HNEE', '1CGHA', '1FUJA', '1ORFA', '3FZZA', 
            '2ZGCA', '3RP2A', '2F9PA', '1MZAA', '2RDLA', '1JRSA', '2JETB', '1ELCA', '1EKBB', 
            '1PYTC', '3DFJA', '2ZCHP', '1SGFG', '1GVZA', '1TONA', '1AO5A', '2R9PC', 
            '1MD7A', '1ELVA', '2ODPA', '3GOVA', '2OLGA', '1ZJDA', '1PFXC', '1DANH',
            '1HCGA', '1ABJH', '1AUTC', '1FIZA', '1O5FL', '1YBWA', '1Q3XA', '1MLWA',
            '1BUIA', '1LO6A', '1YM0A', 
            '1NPMA', '2BDGA', '1SGCA', '1SGPE', 
            '1HPGA', '2ALPA', '1QY6A', '1EXFA', '1KY9A', '1SO7A', '1LCYA', '1ARCA',
            '2VIDA', '2AS9A', '2QXIA', '2GV6A', '2SFAA', '1EQ9A', '1P3EA', 
            '2AIQA', '1L1JA', '2XXLA', '1SGFA', '2PFEA'
           ],
    'S03': ['2SNVA'],
    'S06': ['1WXRA'],
    'S29': ['1A1RA'],
    'S32': ['1MBMA'],
    'S39': ['1ZYOA'],
}


for family, pdb_list in pa_proteins.items():
    for p in pdb_list:
        result_set = get_dali_query(p)

        # Write out new data
        outdir = './dali_dataset/' + family
        if not os.path.exists(outdir):
            os.mkdir(outdir)
             
        with open(outdir + '/' + p + '.txt', 'w') as f:
            p_reformatted = p[:4].lower() + '-' + p[4]
            f.write(p_reformatted + '\n')
            f.writelines(m + '\n' for m in result_set)
            
        del result_set[:]

        print('Got result set for {}'.format(p))

protein_files = []
for root, dirs, files in os.walk("dali_dataset"):
    for file in files:
        if file.endswith(".txt"):
             protein_files.append(os.path.join(root, file).replace('\\', '/'))

agg_prot = set()
for path in protein_files:
    with open(path, 'r') as f:
        prot_per_file = f.readlines()
        agg_prot.update([p.strip() for p in prot_per_file])

agg_prot_list = list(agg_prot)
agg_prot_list.sort()

print(len(agg_prot_list))

with open("dali_pa_neighbors.txt", "w") as f_out:
    f_out.writelines(p + '\n' for p in agg_prot_list)

