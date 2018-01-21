import requests
import json
import re
import gzip
import pandas as pd
import tarfile
import os
import sys
import shutil

def gdc_query(cancer):
    files_endpt = "https://api.gdc.cancer.gov/files"

    filters = {
        "op": "and",
        "content":[
            {
            "op": "in",
            "content":{
                "field": "cases.project.project_id",
                "value": ["TCGA-"+cancer]
                }
            },
            {
            "op": "in",
            "content":{
                "field": "files.experimental_strategy",
                "value": ["RNA-Seq"]
                }
            },
            {
            "op": "in",
            "content":{
                "field": "files.analysis.workflow_type",
                "value": ["HTSeq - Counts"]
                }
            }
        ]
    }

    # Here a GET is used, so the filter parameters should be passed as a JSON string.

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id",
        "format": "JSON",
        "size": "10"
        }

    response = requests.get(files_endpt, params = params)

    file_uuid_list = []

    # This step populates the download list with the file_ids from the previous query
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        file_uuid_list.append(file_entry["file_id"])

    data_endpt = "https://api.gdc.cancer.gov/data"

    params = {"ids": file_uuid_list}

    response = requests.post(data_endpt, data = json.dumps(params), headers = {"Content-Type": "application/json"})

    response_head_cd = response.headers["Content-Disposition"]

    file_name = re.findall("filename=(.+)", response_head_cd)[0]

    with open(file_name, "wb") as output_file:
        output_file.write(response.content)

    return file_name


    #with gzip.open(file_name, 'rb') as f:
      #  file_content = f.read()
	  
def wrapper(file_name):

    tar = tarfile.open(file_name)
    tar.extractall("./temp")

    count = 0
    for root, subdirs, files in os.walk('temp'):
        if files[0][-3:] == '.gz':
            with gzip.open(root +'\\'+ files[0], 'rb') as f:
                file_content = f.read()
                exp = file_content.decode("utf-8")
                file = open("tempfile" + str(count) + ".txt","w")
                file.write(exp)
        count = count + 1

    df = None
    for i in range(1,11):
        df = pd.concat([df,pd.read_table('tempfile'+ str(i) + '.txt', header=None, sep='\t')], axis=1)
		
    df = df.drop(df.columns[[2, 4, 6,8,10,12,14,16,18]], axis=1)
		
	#Delete temporary file and directory
    #os.remove(file_name)
    #shutil.rmtree('.\temp')
    #for i in range(1,11):
	#    os.remove('tempfile'+str(i)+'.txt')
    df = df.head()
    df = df.to_html(header=None)
    df = df[36:]
    df = '<table class="table table-striped">'+df
	
    return df

if __name__ == '__main __':
		
    file_name = gdc_query(cancer)
		
    wrapper(file_name)

