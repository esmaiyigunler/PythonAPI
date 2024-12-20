from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)


connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=PAPATYA\\SQLEXPRESS01;"
    "Database=kullaniciYonetimi;"
    "Trusted_Connection=yes;"
)
cursor = connection.cursor()

@app.route('/kullaniciYonetimi', methods=['GET'])
def get_kullaniciYonetimi():
    cursor.execute("SELECT * FROM Users")
    Users=[{
        "UserID":row[0],
        "Username":row[1],
        "Email":row[2],
        "Password":row[3]
      }
      for row in cursor.fetchall()
    ]
    return jsonify(Users)



@app.route("/kullaniciYonetimi", methods=["POST"])
def post_kullaniciYonetimi():
    data = request.get_json()
    cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)", data['Username'], data['Email'], data['Password'])
    connection.commit()
    return jsonify({"message": "Müşteri eklendi"}), 201

@app.route('/kullaniciYonetimi/<int:UserID>',methods=['PUT'])
def getkullaniciYonetimi(UserID):
    data=request.get_json()
    cursor.execute("UPDATE Users SET Username=?, Email=?, Password=? WHERE UserID=?",data.get('Username'), data.get('Email'), data.get('Password',False), UserID)
    connection.commit()
    return jsonify({"message": "Müşteri güncellendi"}), 201


@app.route('/kullaniciYonetimi/<int:UserID>', methods=['DELETE'])
def delete_kullaniciYonetimi(UserID):
    cursor.execute("DELETE FROM Users WHERE UserID = ?", UserID)
    connection.commit()
    return jsonify({"message": "Müşteri silindi"}), 200


if __name__ == '__main__':
    app.run(debug=True)






























