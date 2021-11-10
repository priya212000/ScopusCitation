import requests
import json

# #checking number of requests remaining
# url = "https://api.elsevier.com/content/abstract/scopus_id/85040730407?apiKey=24783270e58eb56ff94c059e8c7eb44c"
# response = requests.get(url)
# print(response.headers)

print("How would you like to retrieve information?")
print("1. ORCID")
print("2. Author ID")
print("3. EID")
c = int(input("Enter choice: "))
try:
    if c==1:
        n = input("Enter ORCID: ")
        url = "http://api.elsevier.com/content/author?orcid=" + n + "&view=metrics"
        resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
    elif c==2:
        n = input("Enter Author ID: ")
        url = "http://api.elsevier.com/content/author?author_id=" + n + "&view=metrics"
        resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
    elif c==3:
        n = input("Enter EID ID: ")
        url = "http://api.elsevier.com/content/author?eid=" + n + "&view=metrics"
        resp = requests.get(url, headers={'Accept':'application/json','X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
    else:
        print("Invalid choice!")
        quit(keep_kernel=True)

    #Remove &view=metrics to get all information

    out = (json.dumps(resp.json(),
                     sort_keys=True,
                     indent=4, separators=(',', ': ')))
    out1 = dict(resp.json())
    if list(out1)[0]=="service-error":
        print("SERVICE ERROR!")
    else:
        print("CITATION COUNT:" + str(out1['author-retrieval-response'][0]['coredata']['citation-count']))
except:
    print("Connect to a valid network")
