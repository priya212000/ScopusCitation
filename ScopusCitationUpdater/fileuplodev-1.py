from flask import Flask, render_template, request, make_response
import requests
import csv
import os
import weasyprint
import json

app = Flask(__name__)

@app.route('/')
def uploadfile():
   return render_template('upload.html')
	
@app.route('/uploader',methods=['GET','POST'])
def getpostmet():
    if request.method=='GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        if file:
            file.stream.seek(0)
            myfile=file.read().decode("utf-8")
            data=csv.reader(myfile.split('\n'),delimiter=',')
            generated=[]
            for info in data:
                #code for getting citation  :  todo

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
                        generated.append([info[0],respdat['author-retrieval-response'][0]['coredata']['citation-count']])

                #generated.append(info)
                #append profassor info and citation to genetated
            pdf_outline=render_template('pdf_template.html',result=generated)
    
            pdf=weasyprint.HTML(string=pdf_outline).write_pdf()
    
            resp=make_response(pdf)
            resp.headers['Content-Type']="application/pdf"
            resp.headers['Content-Disposition']="inline;filename=Citations.pdf"
    
            return resp
        else:
            return render_template('upload.html')
        
if __name__ == '__main__':
   app.run(debug = True)