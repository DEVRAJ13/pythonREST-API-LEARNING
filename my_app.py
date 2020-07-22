from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'python_test_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'name' and 'email' and 'pwd':
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']
    if(len(_name) == 0):
        return jsonify("User can't be empty!")
    elif(len(_email) == 0):
        return jsonify("Email can't be empty!")
    elif(len(_password) == 0):
        return jsonify("Password can't be empty!")
    else:
        sql = "SELECT * FROM tbl_user WHERE user_email = %s"
        data = (_email)
        cur = mysql.connect().cursor()
        cur.execute(sql, data)
        account = cur.fetchone()
    if account:
        return jsonify('User already exist!')
    else:
        _hashed_password = generate_password_hash(_password)
        sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
        data = (_name, _email, _hashed_password)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('User created successfully!')
        resp.status_code = 200
        return resp


@app.route('/users', methods=['GET'])
def get():
    cur = mysql.connect().cursor()
    cur.execute('''select * from tbl_user''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'body': r})


@app.route('/user/<int:id>')
def user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run()
