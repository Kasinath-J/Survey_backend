from apiclient import discovery
from google.oauth2 import service_account

scopes = ['https://www.googleapis.com/auth/spreadsheets']
secret_file = r"D:\Projects\6.Survey\Survey_backend\client_secret.json"
credentials = service_account.Credentials.from_service_account_file(secret_file,scopes=scopes)
service = discovery.build('sheets','v4',credentials=credentials)


spreadsheet_id='1KINif-eSxxILPJrrxthxOcmmBkeSyBQRvW9vtD1sHT4'
range_name = 'Sheet1!A1:B5'
data ={
    'values':[['hello']]
}
# service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()
response= service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
response = response['values']
print(response)