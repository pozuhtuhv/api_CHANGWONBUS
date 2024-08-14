import json

# # 버스 행정구역
# gov_list = []
# with open('data/[1-1]busdata.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
# rows = data["ServiceResult"]["MsgBody"]["BusList"]["row"]

# for row in rows:
#     if row['GOV_NM'] in gov_list:
#         pass
#     else:
#         gov_list.append(row['GOV_NM'])
# print(gov_list)

# 버스 정보
busnum = input("버스 노선을 입력하세요: ")

with open('data/[1-1]busdata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

rows = data["ServiceResult"]["MsgBody"]["BusList"]["row"]
for row in rows:
    if row['ROUTE_NM'] == busnum:
        pretty_row = json.dumps(row, indent=4, ensure_ascii=False)
        print(pretty_row)