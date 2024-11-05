from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_restful import Resource, Api
from sql_7 import *
from tools.binarySearch import *

# pip install Flask-Session

app=Flask(__name__)
api = Api(app)
app.secret_key = "super secret key"

u = "https://elms1.skinfosec.co.kr:8082/community6/free"
h = {
    "Content-Type": "application/x-www-form-urlencoded"
}
c = {
    "JSESSIONID":"sessionid"
}
d = {
    "startDt":"",
    "endDt":"",
    "searchType":"all",
    "keyword":"EQST%' and (공격쿼리) and '1%'='1"
}


@app.route("/")
def index(): 
    session.pop('jsession', None)
    return render_template("index.html")


@app.route("/submit", methods=['POST'])
def submit():
    jsessionid = request.form.get('user_input') 
    print(f"{jsessionid}")

    session["jsessionid"] = jsessionid

    set_sessionid(session["jsessionid"])

    return redirect('/home')


@app.route("/home", methods=['GET'])
def home():

    if not "jsessionid" in session:
        flash("세션 id를 입력해야 합니다.")
        return redirect("/")
  
    return redirect("/table")



@app.route("/table", methods=['GET'])
def get_table():
    table_count = get_table_count()
    table_name_list = get_table_name(table_count)
    return render_template("table.html")

@app.route("/column/<table_name>", methods=['GET'])
def get_column():
    table_name = request.args.get('table_name','none')
    column_count = get_column_count(table_name)
    column_name_list = get_coloumn_name(column_count, table_name)
    return render_template("column.html")

@app.route("/data/<table_name>/<column_name>", methods=['GET'])
def get_data():
    table_name = request.args.get('table_name','none')
    column_name = request.args.get('column_name','none')

    data_count = get_data_count(table_name, column_name)
    data_list = get_data(table_name, column_name, data_count)
    return render_template("data.html")



def set_sessionid(jsessionid):
    c = {
        "JSESSIONID":f"{jsessionid}"
    }
    






# api.insert_session_id(TodoList, '/todos')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)