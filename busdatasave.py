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

    # [1-1]busdata 파일을 대표로 마지막 시간을 확인
    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime('data/[1-1]busdata.json'))
    if modified_time < six_hours_ago:  
        data_save()
    else:
        print('No reload required')

# 실행시 무조건 실행
newdata_load()


# 버스정보검색 ([1-3]stationdata.json 연동 필요)
bus = input('버스번호검색: ')
# json 데이터 로드
with open('data/[1-1]busdata.json', 'r', encoding='utf-8') as file:
    rows = json.load(file)["ServiceResult"]["MsgBody"]["BusList"]["row"]

# 검색 결과 출력
matching_buses = [row for row in rows if bus in str(row["ROUTE_NM"])]

for bus_info in matching_buses:
    print(bus_info["ROUTE_NM"])

# 사용자 선택
selected_bus = input('선택: ')

# 선택한 버스 정보 출력
for bus_info in matching_buses:
    if selected_bus == str(bus_info["ROUTE_NM"]):
        print(bus_info)

# ##############################
# # 3006번의 버스 - 379030060
# ROUTE_ID = '379030060'
# STATION_ID = '379005774'
# url = f'http://openapi.changwon.go.kr/rest/bis/BusArrives/?serviceKey={SERVICE_KEY}&station={STATION_ID}'
# response = requests.get(url)
# xml_data = response.content.decode('utf-8') # 한글 디코딩이 필요함
# json_data = json.dumps(xmltodict.parse(xml_data), indent=4, ensure_ascii=False)

# # json 저장
# with open('data/[2-1]busarrives.json', 'w', encoding='utf-8') as file:
#     file.write(json_data)

# # json 읽기
# with open('data/[2-1]busstop.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# rows = data["ServiceResult"]["MsgBody"]["BusLocationList"]["row"]

# for row in rows:
#     print(row)