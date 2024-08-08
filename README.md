# api_CHANGWONBUS

## Changwonbus API
* Protocol : REST
* Origin Data format : XML
* Data 

## API DATA INFORMATION

### 1. [경상남도 창원시_버스도착정보조회](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000386)
   - [2] 정류소버스도착정보 (http://openapi.changwon.go.kr/rest/bis/BusArrives/?serviceKey={SERVICE_KEY}&station={STATION_ID})
      - ROUTE_ID : 버스 고유번호
      - PREDICT_TRAV_TM : 버스도착예정시간
      - LEFT_STATION : 남은 정류소 수
      - UPDN_DIR : 상하행 구분 (0 하행 ,1 상행) 
        - 기점 가는길이 상행
        - 종점 가는길이 하행
  
### 2. [경상남도 창원시_기반정보조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000096)
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
