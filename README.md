# 창원버스 API 문서

## 개요
- **프로토콜**: REST
- **데이터 형식**: XML

## API 엔드포인트 및 반환정보

### 1. 버스 및 정류소 데이터 

- **[경상남도 창원시_기반정보조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000096)**

- **버스노선목록 - [1-1]busdata.json**
  - **엔드포인트**: `http://openapi.changwon.go.kr/rest/bis/Bus/?serviceKey={SERVICE_KEY}`
  - **반환 정보 (필요한것만)**:
    - `ROUTE_ID`: 버스 고유 ID
    - `ROUTE_NM`: 버스 번호
    - `STATION_CNT`: 정류장 수
    - `ROUTE_LEN`: 노선 길이
    - `ORGT_STATION_ID`: 기점 정류장 ID
    - `DST_STATION_ID`: 종점 정류장 ID

- **정류소목록 - [1-3]stationdata.json**
  - **엔드포인트**: `http://openapi.changwon.go.kr/rest/bis/Station/?serviceKey={SERVICE_KEY}`
  - **반환 정보 (필요한것만)**:
    - `STATION_ID`: 정류소 고유 ID
    - `STATION_NM`: 정류소 이름

### 2. 버스 도착 정보

- **[경상남도 창원시_버스도착정보조회](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000386)**

- **정류소버스도착정보**
  - **엔드포인트**: `http://openapi.changwon.go.kr/rest/bis/BusArrives/?serviceKey={SERVICE_KEY}&station={STATION_ID}`
  - **반환 정보 (필요한것만)**:
    - `ROUTE_ID`: 버스 고유 ID
    - `PREDICT_TRAV_TM`: 도착 예정 시간
    - `LEFT_STATION`: 남은 정류장 수
    - `UPDN_DIR`: 상/하행 구분 (0: 하행, 1: 상행)

### 3. 버스정류소목록

- **[경상남도 창원시_노선버스위치정류소](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000254)**

- **버스정류소목록 - [3-1]busstop.json**
  - **엔드포인트**: `http://openapi.changwon.go.kr/rest/bis/BusLocation/?serviceKey={SERVICE_KEY}&route={ROUTE_ID}`
  - **반환 정보 (필요한것만)**:
    - `rowCount`: 결과 개수 | (총결과/2)+1 = 상행/하행 구분하기 
    - `STATION_ORD`: 정류장 순서
    - `STATION_ID`: 정류소 고유 ID
    - `STATION_NM`: 정류소 이름
    - `EVENT_CD`: 이벤트 코드 (17: 진입, 18: 진출)

### 4. 현재 운행 버스위치

- **[경상남도 창원시_노선별 버스위치목록](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000416)**

- **현재 운행 버스위치 - [4-1]busposition.json**
  - **엔드포인트**: `http://openapi.changwon.go.kr/rest/bis/BusPosition/?serviceKey={SERVICE_KEY}&route={ROUTE_ID}`
  - **반환 정보 (필요한것만)**:
    - `rowCount`: 결과 개수
    - `ARRV_STATION_ID`: 도착한 정류장 ID
    - `LOW_PLATE_TP`: 저상버스 여부
    - `PLATE_NO`: 차량 번호

## PLAN

### PLAN 1: 현재 버스 위치와 다음 정류장 조회

- **STEP 1** : `[1-1]busdata.json`과 `[1-3]stationdata.json` 데이터를 수집.
- **STEP 2** : 입력된 버스 번호(`ROUTE_NM`)를 `[1-1]busdata.json`에서 버스 고유 ID(`ROUTE_ID`)로 매칭.
- **STEP 3** : 버스 고유 ID(`ROUTE_ID`)를 사용해 `BusPosition` API로 현재 버스 위치를 조회.
- **STEP 4** : `[3-1]busstop.json`을 사용해 현재 버스 위치의 다음 정류장을 조회.

### PLAN 2: 정류소 검색 -> 상/하행 정류소 목록 조회 -> 도착 정보 조회

- **STEP 1** : `[1-3]stationdata.json` 데이터를 수집.
- **STEP 2** : 입력된 정류소이름(`STATION_NM`)을 통해 정류소 검색 후 목록나열
- **STEP 3** : 선택된 정류소 고유 ID(`STATION_ID`)를 반환.
- **STEP 4** : 정류소 고유 ID(`STATION_ID`)를 사용해 도착 예정 버스 정보를 조회.

### PLAN 3: JavaScript와 HTML을 사용한 출력

- **목적**: JavaScript와 HTML을 사용하여 위의 결과를 사용자 친화적인 방식으로 출력.

## 주의사항 및 개선점
- **오류 처리**: API 호출 시 잘못된 서비스 키, 네트워크 문제 등 다양한 오류 상황에 대비한 처리 필요.
- **성능 최적화**: `[1-1]busdata.json` 및 `[1-3]stationdata.json`와 같은 자주 사용되는 데이터를 캐싱하여 API 호출을 최소화.
- **보안**: `SERVICE_KEY`를 클라이언트 코드에서 직접 노출하지 않도록 주의.
- **UI/UX**: React나 Vue와 같은 최신 JavaScript 프레임워크를 사용하여 보다 동적이고 반응적인 사용자 경험 제공 고려.
