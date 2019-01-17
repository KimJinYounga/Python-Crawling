from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def saveImage(fileName):
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("make new storage data file ")
        flow = client.flow_from_clientsecrets('client_secret2.json', SCOPES) # 서비스 계정 키 json 형식으로 저장
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    # 폴더 생성
    # 이름을 바꾸려면 kakao를 변경하면 됨
    # 폴더가 새로 생성됨
    folder_metadata = {
        'name': 'kakao',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = DRIVE.files().create(body=folder_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % folder.get('id'))

    # 기존 폴더를 사용할 경우 위에 만들어진 폴더 아이디를 folder.get('id') 부분에 넣으면 됨
    file_metadata = \
        {
        'name': fileName,
        'parents' : [folder.get('id')]
                     }

    media = MediaFileUpload(fileName,
                            mimetype='image/jpeg')
    fileId = DRIVE.files().create(body=file_metadata,
                                media_body=media).execute()
    print('File ID: %s' % fileId.get('id'))
    return fileId.get('id')
