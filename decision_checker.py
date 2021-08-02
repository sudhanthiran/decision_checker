"""
Strictly developed to help students, not for anyother purpose.

"""
#!pip install requests,tabula-py,beautifulsoup4,pandas

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
import tabula
from bs4 import BeautifulSoup

def download_and_process_pdf(link: str,ref_no : int) -> dict:
    result_dict = {}
    tables = tabula.read_pdf(link, pages="all", multiple_tables=False,output_format="dataframe")
    result_df = tables[0][tables[0]["Application\rNumber"]==ref_no]

    if (result_df.shape[0] == 1):
        result_dict["flag"] = 1
    else:
        result_dict["flag"] = 0
    return dict(result_dict,**(result_df.to_dict()))

def process_pdf(html_obj: BeautifulSoup,ref_no : int,base_url : str = 'https://dfa.ie') -> dict:
    result ={ "title" : html_obj.a.text,
              "link" : base_url + str(html_obj.a["href"]),
              "found" : "N"
    }
    print(fr"Searching IRL{ref_no} in {result['title']}")

    dict_resp = download_and_process_pdf(link=result["link"],ref_no=ref_no)
    if (dict_resp["flag"] == 1):
        result["found"] = "Y"

    return dict(result, **(dict_resp))

ref_no = int(input("Enter your IRL ref number (without IRL)"))

base_url = 'https://dfa.ie'
visa_decision_url = "/irish-embassy/india/visas/processing-times-decisions-appeals/discoverytabbody2/#d.en.325193"

data= requests.get(base_url+visa_decision_url,verify=False)

soup = BeautifulSoup(data.text,'html.parser')
decisions_pdf = soup.find_all('div',class_= "gen-content-landing__block")
decisions_pdf = decisions_pdf[1:]
result={}

#print(decisions_pdf)
for i in decisions_pdf:
    result = process_pdf(html_obj=i,ref_no=ref_no)

    if (result["found"]=="Y"):
        break

print(result)
