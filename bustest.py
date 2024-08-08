import json
import os

import requests
import xmltodict
from dotenv import load_dotenv

# .env 파일 활성화
load_dotenv()
SERVICE_KEY = os.getenv('SERVICE_KEY')

# 창원버스 정보제공 API는 데이터 포맷이 XML 이므로 JSON 변환 과정 추가

# URL 리스트 정의
API_URLS = {
    'busdata': f'http://openapi.changwon.go.kr/rest/bis/Bus/?serviceKey={SERVICE_KEY}',
    'stationdata': f'http://openapi.changwon.go.kr/rest/bis/Station/?serviceKey={SERVICE_KEY}'
}

# XML 데이터를 가져와 JSON으로 변환 후 파일에 저장
def fetch_and_save_data(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_data = response.content.decode('utf-8')
        json_data = json.dumps(xmltodict.parse(xml_data), indent=4, ensure_ascii=False)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_data)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
    except Exception as e:
        print(f"Error processing XML data: {e}")

# 데이터 저장
def data_save():
    for filename, url in API_URLS.items():
        fetch_and_save_data(url, f"data/{filename}.json")

data_save()