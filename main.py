from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api

app=Flask(__name__)
api = Api(app)

@app.route("/submit", method=['POST'])
def submit():
    jsessionid = request.form.get('user_input') 
    print("사용자 정보 확인 . . . . .")
    print(f"{jsessionid}")
    return jsessionid

api.insert_session_id(TodoList, '/todos')

if __name__ == 'main':
    app.run('0.0.0.0', port=5001, debug=True)