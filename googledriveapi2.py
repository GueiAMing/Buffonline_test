from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta, timezone
import configparser
import json
config = configparser.RawConfigParser()
config.read('/home/linebot008/Buffonline/config.ini')

UPLOAD_FOLDER = config.get('googledriveapi', 'upload_folder')
SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = json.dumps({
#   "type": config.get('GoogleDriveAPI', "type"),
#   "project_id": config.get('GoogleDriveAPI', "project_id"),
#   "private_key_id": config.get('GoogleDriveAPI', "private_key_id"),
#   "private_key": config.get('GoogleDriveAPI', "private_key"),
#   "client_email": config.get('GoogleDriveAPI', "client_email"),
#   "client_id": config.get('GoogleDriveAPI', "client_id"),
#   "auth_uri": config.get('GoogleDriveAPI', "auth_uri"),
#   "token_uri": config.get('GoogleDriveAPI', "token_uri"),
#   "auth_provider_x509_cert_url": config.get('GoogleDriveAPI', "auth_provider_x509_cert_url"),
#   "client_x509_cert_url": config.get('GoogleDriveAPI', "client_x509_cert_url"),
#   "universe_domain": config.get('GoogleDriveAPI', "universe_domain")
# })
SERVICE_ACCOUNT_FILE ='/home/linebot008/Buffonline/google_auth.json'
  # 金鑰檔案



# 建立憑證物件
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

tzone = timezone(timedelta(hours=8))
nowtime = datetime.now(tz=tzone).isoformat()[:16]
nowtime = nowtime.split("T")
dbyeardate = nowtime[0].replace("-","")[2:]
time = nowtime[1]
filename = f"/home/linebot008/Buffonline/Data/final_order_{dbyeardate}.csv"    # 上傳檔的名字
media = MediaFileUpload(filename)
file = {'name': f"final_order_{dbyeardate}_{time}.csv", 'parents': [UPLOAD_FOLDER]}

print(f"正在上傳檔案...{time}")
file_id = service.files().create(body=file, media_body=media).execute()
print('雲端檔案ID：' + str(file_id['id']))

filename = "/home/linebot008/Buffonline/Data/temp_order.csv"
media = MediaFileUpload(filename)
file = {'name': f"temp_order_{time}.csv", 'parents': [UPLOAD_FOLDER]}

print(f"正在上傳檔案...{time}")
file_id = service.files().create(body=file, media_body=media).execute()
print('雲端檔案ID：' + str(file_id['id']))

filename = "/home/linebot008/Buffonline/Data/userid_yeardate_time.csv"
media = MediaFileUpload(filename)
file = {'name': f"userid_yeardate_time_{time}.csv", 'parents': [UPLOAD_FOLDER]}

print(f"正在上傳檔案...{time}")
file_id = service.files().create(body=file, media_body=media).execute()
print('雲端檔案ID：' + str(file_id['id']))