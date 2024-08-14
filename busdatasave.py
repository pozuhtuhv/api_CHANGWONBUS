import os
import requests
import xmltodict
import json
from dotenv import load_dotenv
import datetime

# .env 파일 로드
load_dotenv()
SERVICE_KEY = os.getenv('SERVICE_KEY')

# 창원버스 정보제공 API는 데이터 포맷이 XML 이므로 JSON 변환 과정 추가

# URL 리스트 정의 BUS, STATION DATA LOAD [1-1], [1-3] 데이터 로드
API_URLS = {
    '[1-1]busdata': f'http://openapi.changwon.go.kr/rest/bis/Bus/?serviceKey={SERVICE_KEY}',
    '[1-3]stationdata': f'http://openapi.changwon.go.kr/rest/bis/Station/?serviceKey={SERVICE_KEY}'
}

# XML 데이터를 가져와 JSON으로 변환 후 파일에 저장
# 데이터 로드 영역 22 ~ 58
def fetch_and_save_data(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_data = response.content.decode('utf-8') # 한글 디코딩이 필요함
        json_data = json.dumps(xmltodict.parse(xml_data), indent=4, ensure_ascii=False)
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_data)

    except requests.exceptions.RequestException as e:
        print(f'{url}에서 데이터 가져올 수 없습니다.: {e}')
    except Exception as e:
        print(f'XML 데이터 처리 중 오류가 발생했습니다.: {e}')

def data_save():
    for filename, url in API_URLS.items():
        print('older than 6 hours, reloading...')
        fetch_and_save_data(url, f'data/{filename}.json')
        print('reload Done')

def newdata_load():
    # 데이터의 6시간 기준 최신화를 위한 리로드
    # 6시간 전의 현재 시간
    six_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=6)

    # data/ 폴더 내의 모든 파일을 찾습니다.
    files = [os.path.join('data/', f) for f in os.listdir('data/') if os.path.isfile(os.path.join('data/', f))]

    # 각 파일의 마지막 수정일을 확인합니다.
    for file in files:
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        if modified_time < six_hours_ago:  
            data_save()
        else:
            print('No reload required')

newdata_load()

# http://openapi.changwon.go.kr/rest/bis/ROUTEPosition/?serviceKey={SERVICE_KEY}&route={ROUTE_ID}

# ROUTE_ID = input()

# 현재 3006번의 버스 운행 목록
url = f'http://openapi.changwon.go.kr/rest/bis/BusPosition/?serviceKey={SERVICE_KEY}&route=379030060'
response = requests.get(url)
xml_data = response.content.decode('utf-8') # 한글 디코딩이 필요함
json_data = json.dumps(xmltodict.parse(xml_data), indent=4, ensure_ascii=False)

with open('data/[4-1]busposition.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

with open('data/[4-1]busposition.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

rows = data["ServiceResult"]["MsgBody"]["BusPositionList"]["row"]

for row in rows:
    print(row)