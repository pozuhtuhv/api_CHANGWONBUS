# api_CHANGWONBUS

## Changwonbus API
* Protocol : REST
* Origin Data format : XML
* Data 

## API DATA INFORMATION

### 1. BUS, STATION DATA LOAD (busdata.json, stationdata.json)
#### 1. [경상남도 창원시_기반정보조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000096)
   - [1] 버스노선목록 (http://openapi.changwon.go.kr/rest/bis/Bus/?serviceKey={SERVICE_KEY})
      - ROUTE_ID : 버스 고유번호
      - ROUTE_NM : 버스 실제번호
      - STATION_CNT : 정류장 수
      - ROUTE_LEN : 노선길이
      - ORGT_STATION_ID : 종점번호
      - DST_STATION_ID : 종점번호
   - [3] 정류소목록 (http://openapi.changwon.go.kr/rest/bis/Station/?serviceKey={SERVICE_KEY})
      - STATION_ID : 정류소 고유번호
      - STATION_NM : 정류소 실제이름

### 2. ARRIVEINFO LOAD
#### 1. [경상남도 창원시_버스도착정보조회](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000386)
   - [2] 정류소버스도착정보 (http://openapi.changwon.go.kr/rest/bis/BusArrives/?serviceKey={SERVICE_KEY}&station={STATION_ID})
      - ROUTE_ID : 버스 고유번호
      - PREDICT_TRAV_TM : 버스도착예정시간
      - LEFT_STATION : 남은 정류소 수
      - UPDN_DIR : 상하행 구분 (0 하행 ,1 상행) 
         - 기점 가는길이 상행
         - 종점 가는길이 하행

### 3. STATION Position INFO LOAD
#### 1. [경상남도 창원시_노선버스위치정류소](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000254)
   - [1] 노선버스위치정류소 (http://openapi.changwon.go.kr/rest/bis/BusLocation/?serviceKey={SERVICE_KEY}&route={ROUTE_ID})
      - rowCount : 결과 row 갯수
      - STATION_ORD : 몇번째 정류장
      - STATION_ID : 정류소 고유번호
      - STATION_NM : 정류소 실제이름
      - EVENT_CD : 17 : 진입, 18 : 진출

### 4. BUS Position INFO LOAD
#### 1. [경상남도 창원시_노선별 버스위치목록](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000416)
   - [1] 노선별 버스위치목록 : 해당 버스의 현재 위치 (http://openapi.changwon.go.kr/rest/bis/BusPosition/?serviceKey={SERVICE_KEY}&route={ROUTE_ID})
      - rowCount : 결과 row 갯수
      - ARRV_STATION_ID : 도착한 정류장 아이디
      - LOW_PLATE_TP : 저상버스 유무
      - PLATE_NO : 차량 번호

---

### PLAN
#### PLAN [1] : 실제버스번호를 INPUT -> 현재 버스위치 리턴, 다음 정류소 리턴
   - [1-1-1][busdata], [1-1-3][stationdata] 데이터를 수집
   - INPUT의 실제버스번호에서 [1-1-1][busdata] 받아온 데이터의 [ROUTE_NM]를 [ROUTE_ID]와 매칭하여 [ROUTE_ID] 를 리턴
   - [4-1-1][busposition] 데이터에서 현재 버스 위치를 리턴
   - [ROUTE_ID]의 현재 버스 위치의 다음 정류장을 [1-1-3][stationdata] 에서 리턴
  
#### PLAN [2] : 정류장검색 -> 상행하행구분 정류소 목록 -> 선택 -> 정류소 도착정보
   - [1-1-3][stationdata] 데이터를 수집
   - INPUT의 STATION_NM을 통해 목록 나열
   - 나열된 정류소 목록에서 선택 후 STATION_ID 리턴 [2-1-2]번 STATION_ID 검색 후 도착예정인 버스의 [1-1-1][busdata] 데이터에서 [ROUTE_ID] 를 [ROUTE_NM] 로 리턴

#### PLAN [3] : Javescript, html 적용 출력