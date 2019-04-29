import requests
from lxml import html
import re
from collections import OrderedDict
import pandas as pd

"""
https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm
https://www.sec.gov/Archives/edgar/data/51143/



Directory Browsing
Directory browsing is allowed for CIK and Accession Number directories. For example:

https://www.sec.gov/Archives/edgar/data/51143/
https://www.sec.gov/Archives/edgar/data/51143/000104746917001061/
Each CIK directory and all child subdirectories contain 3 files to assist in automated crawling of these directories. (Note that these are not visible through directory browsing.)

index.html (the web browser would normally receive these)
index.xml (a XML structured version of the same content)
index.json (a JSON structured vision of the same content)
Important Note: The /Archives/edgar/data/ directory is not browsable.
"""

def get_urls():
    files = ['company.idx', 'xbrl.idx'] #'crawler.idx', 'form.idx', '
    base = r'https://www.sec.gov/Archives/edgar/full-index/{yr}/QTR{q}/'
    urls = []

    for i in range(2000,2020):
        for q in range(1, 5):
            for f in files:
                urls.append(base.format(yr=i, q=q) + f)
    return urls 


def parse(tst, delimiter='|'):
    #tst = urls_data['https://www.sec.gov/Archives/edgar/full-index/2014/QTR2/xbrl.idx']
    d = [x.split(delimiter) for x in tst.text.split('\n') if len(x.split(delimiter) ) > 2]
    d = [[y.strip() for y in x if y.strip() != ''] for x in d]
    d = [x for x in d if len(x) > 2]
    
    data = []
    
    for row in d[1:]:
        while len(row) > len(d[0]):
            row[0] = row[0] + ' ' + row[1]
            del row[1]
        data.append(row)
    
    df = pd.DataFrame(data, columns=d[0])
    return df



def main():
    full_data = {'xbrl.idx': [], 'company.idx': []}

    for k in urls:
        #print(k)
        f_type = k.split('/')[-1]
        
        r = requests.get(k)
        
        if f_type == 'xbrl.idx':
            df = parse(r, delimiter='|')
        if f_type == 'company.idx':
            df = parse(r, delimiter='  ')
        
        if len(df) > 0:
            df['src_url'] = k
            df['src_type'] = f_type
            full_data[f_type].append(df)
    return full_data 