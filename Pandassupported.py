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
import pandas as pd 
from io import StringIO
from datetime import datetime
import accessFromLocalDB as dbhandle

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
   return render_template('uploaded.html')



@app.route("/getripo",methods=['GET',"POST"])
def getripo():
    generated=dbhandle.get_rowcol()

    si = StringIO()
    csvwriter = csv.writer(si)
    csvwriter.writerows(generated)
    csvfile=si.getvalue()
    resp=make_response(csvfile)
    resp.headers['Content-Type']="text/csv"
    resp.headers['Content-Disposition']="attachment;filename=Citations.csv"
    print("File generated")
    return resp

@app.route("/updateble",methods=['GET'])
def updatable():
    wrap={}
    try:
        dbhandle.updateTables()
        wrap={"stat":"success"}
    except:
        wrap={"stat":"failed"}
    return jsonify( result=wrap)
    
@app.route('/insertFaculty',methods=['GET'])
def stor():
    if request.method == 'GET':
        ID = request.args.get('orcid')
        Name = request.args.get('name')
        try:
            if(ID and len(ID)!=0 and Name and len(Name)!=0):
                res=requests.get("http://api.elsevier.com/content/author",
                                            params={"orcid":ID},
                                            headers={'Accept':'application/json',
                                            'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
                respdat=dict(res.json())
                if list(respdat)[0]=="service-error":
                    print(Name ,"error")
                    wrap={"stat":"failed"}
                else:
                    print(Name ,respdat['author-retrieval-response'][0]['coredata']['citation-count'])
                    print("entering faculty")
                    dbhandle.Enter_Faculty(str(ID),str(Name))
                    wrap={"stat":"success"}
        except:
            wrap={"stat":"failed"}
        return jsonify( result=wrap)
	
@app.route('/uploader',methods=['GET','POST'])
def getpostmet():
    if request.method=='GET':
        return render_template('uploaded.html')
    elif request.method == 'POST':
        buf=io.BytesIO()
        option = request.form['options']
        file = request.files['file']
        if file:
            file.stream.seek(0)
            myfile=file.read().decode("utf-8")
            StringData = StringIO(myfile) 
            data=pd.read_csv(StringData)
            heading=["name","orcid","Citation","Updated on"]
            generated=[heading.copy()]
            data.dropna(inplace=True)

            month=datetime.now().strftime('%B')
            year=datetime.now().year

            concatdate=str(month)+"_"+str(year)
            
            for index, row in data.iterrows():
                if(row['name'] and len(row['name'])!=0 and row['orcid'] and len(row['orcid'])!=0):
                    res=requests.get("http://api.elsevier.com/content/author",
                                        params={"orcid":row['orcid']},
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
                    respdat=dict(res.json())
                    if list(respdat)[0]=="service-error":
                        print(row['name'],"error")
                    else:
                        print(row['name'],respdat['author-retrieval-response'][0]['coredata']['citation-count'])
                        generated.append([row['name'],row['orcid'],respdat['author-retrieval-response'][0]['coredata']['citation-count'],concatdate])

            
            if(option=="p"):
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
                si = StringIO()
                csvwriter = csv.writer(si)
                csvwriter.writerows(generated)
                csvfile=si.getvalue()
                buf.close()
                resp=make_response(csvfile)
                resp.headers['Content-Type']="text/csv"
                resp.headers['Content-Disposition']="attachment;filename=Citations.csv"
                return resp
        else:
            return render_template('uploaded.html')
        



@app.route('/Search',methods=['GET'])
def Search():
    id = request.args.get("orcid")
    option = request.args.get("inputoptions")
    
    if(id and len(id)>0):
        res={}
        
        if option=="o":
            res=requests.get("http://api.elsevier.com/content/author",
            params={"orcid":id},
            headers={'Accept':'application/json',
            'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
        elif option=="a":
            res=requests.get("http://api.elsevier.com/content/author",
            params={"author_id":id},
            headers={'Accept':'application/json',
            'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
        else:
            res=requests.get("http://api.elsevier.com/content/author",
            params={"eid":id},
            headers={'Accept':'application/json',
            'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
        print("retrived ",option)
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
            #pprint(dat['author-retrieval-response'][0]['author-profile']['preferred-name'])
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

@app.route("/chart",methods=['GET','POST'])
def chart():
    return render_template('uploaded.html',label=dbhandle.get_label(),data=dbhandle.formatted())


if __name__ == '__main__':
   app.run()