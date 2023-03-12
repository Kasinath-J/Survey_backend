from apiclient import discovery
from google.oauth2 import service_account
from pathlib import Path
from nested_lookup import nested_lookup
import ast # to convert string to dict
import os

scopes = ['https://www.googleapis.com/auth/spreadsheets']
secret_file = os.path.join(Path(__file__).resolve().parent.parent.parent.parent,r"client_secret.json")
credentials = service_account.Credentials.from_service_account_file(secret_file,scopes=scopes)
service = discovery.build('sheets','v4',credentials=credentials)

# D:\Projects\6.Survey\Survey_backend\client_secret.json



def addGSheet(gid,results,format):
    # try:
        # all_elements=[]
        # for i in nested_lookup('elements', format):
        #     for j in i:
        #         all_elements.append(j['name'])
        
        # results = ast.literal_eval(results)
        # print(gid,results,all_elements)
        # row = []
        
        # for e in all_elements:
        #     if e not in results:
        #         row.append("")
            
        #     else:
        #         row.append(results[e])
            
        data ={
            'values':[[results]]
        }
        print(gid,data)
        range_name = 'Sheet1!A1'
        service.spreadsheets().values().append(spreadsheetId=gid, body=data, range=range_name, valueInputOption='USER_ENTERED',insertDataOption='INSERT_ROWS').execute()


    # except:
    #     print("error")