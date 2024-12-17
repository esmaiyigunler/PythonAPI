from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# SQL Server bağlantı ayarları
connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=PAPATYA\\SQLEXPRESS01;"
    "Database=OnlineMağazaYonetimi;"
    "Trusted_Connection=yes;"
)
cursor = connection.cursor()

#Get methodu

@app.route('/OnlineMağazaYonetimi', methods=['GET'])
def get_OnlineMağazaYonetimi():
    cursor.execute("SELECT * FROM Müşteriler")
    Müşteriler=[{
        "MusteriID":row[0],
        "MusteriAdi":row[1],
        "MusteriSoyadi":row[2],
        "Telefon":row[3]
      }
      for row in cursor.fetchall()
    ]
    return jsonify(Müşteriler)




@app.route("/OnlineMağazaYonetimi", methods=["POST"])
def post_OnlineMağazaYonetimi():
    data = request.get_json()
    cursor.execute("INSERT INTO Müşteriler (MusteriAdi, MusteriSoyadi, Telefon) VALUES (?, ?, ?)", data['MusteriAdi'], data['MusteriSoyadi'], data['Telefon'])
    connection.commit()
    return jsonify({"message": "Müşteri eklendi"}), 201


@app.route('/OnlineMağazaYonetimi/<int:MusteriID>',methods=['PUT'])
def getOnlineMağazaYonetimi(MusteriID):
    data=request.get_json()
    cursor.execute("UPDATE Müşteriler SET MusteriAdi=?, MusteriSoyadi=?, Telefon=? WHERE MusteriID=?",data.get('MusteriAdi'), data.get('MusteriSoyadi'), data.get('Telefon',False), MusteriID)
    connection.commit()
    return jsonify({"message": "Müşteri güncellendi"}), 201


@app.route('/OnlineMağazaYonetimi/<int:MusteriID>', methods=['DELETE'])
def delete_OnlineMağazaYonetimi(MusteriID):
    cursor.execute("DELETE FROM Müşteriler WHERE MusteriID = ?", MusteriID)
    connection.commit()
    return jsonify({"message": "Müşteri silindi"}), 200


if __name__ == '__main__':
    app.run(debug=True)






























