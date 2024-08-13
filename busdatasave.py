import os
import requests
import xmltodict
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
SERVICE_KEY = os.getenv('SERVICE_KEY')

# 창원버스 정보제공 API는 데이터 포맷이 XML 이므로 JSON 변환 과정 추가

# URL 리스트 정의 BUS, STATION DATA LOAD [1-1], [1-3] 데이터 로드
API_URLS = {
    'busdata': f'http://openapi.changwon.go.kr/rest/bis/Bus/?serviceKey={SERVICE_KEY}',
    'stationdata': f'http://openapi.changwon.go.kr/rest/bis/Station/?serviceKey={SERVICE_KEY}'
}

# XML 데이터를 가져와 JSON으로 변환 후 파일에 저장
def fetch_and_save_data(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_data = response.content.decode('utf-8') # 한글이 이상하게 나와서 디코딩이 필요함
        json_data = json.dumps(xmltodict.parse(xml_data), indent=4, ensure_ascii=False)
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_data)

    except requests.exceptions.RequestException as e:
        print(f"{url}에서 데이터 가져올 수 없습니다.: {e}")
    except Exception as e:
        print(f"XML 데이터 처리 중 오류가 발생했습니다.: {e}")

# 데이터 저장
def data_save():
    for filename, url in API_URLS.items():
        fetch_and_save_data(url, f"data/{filename}.json")

data_save()