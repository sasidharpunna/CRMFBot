from flask import Flask, render_template, request
from chatterbot import ChatBot
import pypyodbc as odbc
import re

app = Flask(__name__)
CRMFBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    db_host = 'python1'
    db_name = 'projectdetails'
    db_user = 'sa'
    db_password = 'techm123$'
    mudid='12345'
    weekno = re.findall('\d+',userText)
    req=userText.upper().find('TARGET')

    def get_target_details(required,weekno):
        connection_string = 'DSN=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
        db = odbc.connect(connection_string)
        cur=db.cursor()
        SQL= "select " + required + " from targetdetails where MUDID = '" + mudid +"' and weekno = '" + weekno[0] +"';"
        cur.execute(SQL)
        output=cur.fetchone()
        print(output[0])
        print(type(output))
        print(type(output[0]))
        if output[0] == '':
            res = 'Most likely, you dont have ' + required + ' for week no ' + str(weekno[0])
            print(res)
            return res
        else:
            res = 'Your ' + required + ' for week ' + str(weekno[0]) + ' is ' + str(output[0])
            print(res)
            return res

    if req != -1 and weekno:
        required='target'
        return get_target_details(required,weekno)
         
    elif req == -1 and weekno:
        required='achieved'
        return get_target_details(required,weekno)

    else:
        result = str(CRMFBot.get_response(userText))
        return result


if __name__ == "__main__":
    app.run(host = '172.27.174.156', port=5000)
