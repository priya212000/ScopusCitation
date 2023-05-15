from flask import Flask, render_template, request, make_response,jsonify
from flask_cors import CORS
import requests
import csv
import io
import json
from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from pprint import pprint

ts=TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.blue),
    ('BACKGROUND',(0,1),(-1,-1),colors.lightblue),
    ('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('GRID',(0,0),(-1,-1),1,colors.black)
])

app = Flask(__name__)
CORS(app)

@app.route('/')
def uploadfile():
   return render_template('upload.html')
	
@app.route('/uploader',methods=['GET','POST'])
def getpostmet():
    if request.method=='GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        buf=io.BytesIO()
        file = request.files['file']
        if file:
            file.stream.seek(0)
            myfile=file.read().decode("utf-8")
            data=csv.reader(myfile.split('\n'),delimiter=',')
            generated=[["Name","ORCID","Citation"]]
            for info in data:

                if(info and len(info)!=0 and info[1] and len(info[1])!=0 and info[0] and len(info[0])!=0):
                    res=requests.get("http://api.elsevier.com/content/author",
                                        params={"orcid":info[1]},
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
                    respdat=dict(res.json())
                    if list(respdat)[0]=="service-error":
                        print(info[0],"error")
                    else:
                        print(info[0],respdat['author-retrieval-response'][0]['coredata']['citation-count'])
                        generated.append([info[0],info[1],respdat['author-retrieval-response'][0]['coredata']['citation-count']])
            table=Table(generated)
            table.setStyle(ts)
            pdfcreator=SimpleDocTemplate(buf)
            pdfcreator.build([table])
            pdf=buf.getvalue()
            buf.close()
            resp=make_response(pdf)
            resp.headers['Content-Type']="application/pdf"
            resp.headers['Content-Disposition']="attachment;filename=Citations.pdf"
            return resp
        else:
            return render_template('upload.html')
        
@app.route('/Search',methods=['GET'])
def Search():
    id = request.args.get("orcid")
    
    if(id and len(id)>0):
        res=requests.get("http://api.elsevier.com/content/author",
        params={"orcid":id},
        headers={'Accept':'application/json',
        'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
        dat=dict(res.json())
        if list(dat)[0]=="service-error":
            print(id,"error")
        else:
            try:
                affiliation=dat['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']['afdispname']
            except:
                affiliation="Not Specified"

            try:
                address=dat['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['address-part']
            except:
                address+=""
            try:
                address+=','+dat['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['city']
            except:
                address+=""
            try:
                address+=','+dat['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['state']
            except:
                address+=""
            try:
                address+=","+dat['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['country']
            except:
                address+=""
            try:
                address+=","+dat['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['postal-code']
            except:
                address+=""
            
            try:
                citation=dat['author-retrieval-response'][0]['coredata']['citation-count']
            except:
                citation="Not Specified"


            nam=""
            try:
                nam+=dat['author-retrieval-response'][0]['author-profile']['preferred-name']['given-name']+" "+dat['author-retrieval-response'][0]['author-profile']['preferred-name']['surname']
            except:
                try:
                    nam+=" "+dat['author-retrieval-response'][0]['author-profile']['preferred-name']['indexed-name']
                except:
                    nam+=""
            


            AOE=''
            try:
                for i in range(len(dat['author-retrieval-response'][0]["subject-areas"]['subject-area'])):
                    AOE=AOE+dat['author-retrieval-response'][0]["subject-areas"]['subject-area'][i]["$"]+", "
            except:
                AOE=+''
            pprint(dat['author-retrieval-response'][0]['author-profile']['preferred-name'])
            wrap={
                "stat":"success",
                "indn":nam,
                "aff":affiliation,
                "addr":address,
                "cit":citation,
                "aoe":AOE
            }
            return jsonify( result=wrap)
    wrap={"stat":"failed"}
    return jsonify( result=wrap)


if __name__ == '__main__':
   app.run( )
