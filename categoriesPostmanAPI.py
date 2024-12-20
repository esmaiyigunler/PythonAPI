from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)


connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=PAPATYA\\SQLEXPRESS01;"
    "Database=Categories;"
    "Trusted_Connection=yes;"
)
cursor = connection.cursor()
print("SQL bağlantısı kuruldu")



@app.route('/Categories', methods=['GET'])
def get_Categories():
    cursor.execute("SELECT * FROM kategoriler")
    kategoriler=[{
        "KategoriID":row[0],
        "Ad":row[1],
        "Tanım":row[2]
      }
      for row in cursor.fetchall()
    ]
    return jsonify(kategoriler)




@app.route("/Categories", methods=["POST"])
def post_Categories():
    data = request.get_json()
    cursor.execute("INSERT INTO kategoriler (Ad, Tanım) VALUES (?, ?)", data['Ad'], data['Tanım'])
    connection.commit()
    return jsonify({"message": "Kategori eklendi"}), 201


@app.route('/Categories/<int:KategoriID>',methods=['PUT'])
def getCategories(KategoriID):
    data=request.get_json()
    cursor.execute("UPDATE kategoriler SET Ad=?, Tanım=?,WHERE KategoriID=?",data.get('Ad'), data.get('Tanım'), KategoriID)
    connection.commit()
    return jsonify({"message": "Kategori güncellendi"}), 201

@app.route('/Categories/<int:KategoriID>', methods=['DELETE'])
def delete_Categories(KategoriID):
    cursor.execute("DELETE FROM kategoriler WHERE KategoriID = ?", KategoriID)
    connection.commit()
    return jsonify({"message": "Müşteri silindi"}), 200


if __name__ == '__main__':
    app.run(debug=True)






























