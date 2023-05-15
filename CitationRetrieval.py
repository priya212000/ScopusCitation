import requests
import json

def citeCount(orcid):
    try:
        url = "http://api.elsevier.com/content/author?orcid=" + orcid + "&view=metrics"
        resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
        out1 = dict(resp.json())
        return int(out1['author-retrieval-response'][0]['coredata']['citation-count'])
    except:
        print("connection failed")
