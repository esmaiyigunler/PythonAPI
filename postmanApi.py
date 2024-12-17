from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)


connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=PAPATYA\\SQLEXPRESS01;"
    "Database=AraçKiralamaSistemi;"
    "Trusted_Connection=yes;"
)
cursor = connection.cursor()

#Get methodu

@app.route('/AraçKiralamaSistemi', methods=['GET'])
def get_AraçKiralamaSistemi():
    cursor.execute("SELECT * FROM Araçlar")
    Araçlar=[{
        "AracID":row[0],
        "Marka":row[1],
        "Model":row[2],
        "GunlukUcret":row[3]
      }
      for row in cursor.fetchall()
    ]
    return jsonify(Araçlar)




@app.route("/AraçKiralamaSistemi", methods=["POST"])
def post_AraçKiralamaSistemi():
    data = request.get_json()
    cursor.execute("INSERT INTO Araçlar (Marka, Model, GunlukUcret) VALUES (?, ?, ?)", data['Marka'], data['Model'], data['GunlukUcret'])
    connection.commit()
    return jsonify({"message": "Araç eklendi"}), 201

@app.route('/AraçKiralamaSistemi/<int:AracID>',methods=['PUT'])
def getAraçKiralamaSistemi(AracID):
    data=request.get_json()
    cursor.execute("UPDATE Araçlar SET Marka=?, Model=?, GunlukUcret=? WHERE AracID=?",data.get('Marka'), data.get('Model'), data.get('GunlukUcret',False), AracID)
    connection.commit()
    return jsonify({"message": "Araç güncellendi"}), 201


@app.route('/AraçKiralamaSistemi/<int:AracID>', methods=['DELETE'])
def delete_AraçKiralamaSistemi(AracID):
    cursor.execute("DELETE FROM Araçlar WHERE ID = ?", AracID)
    connection.commit()
    return jsonify({"message": "Araç silindi"}), 200


if __name__ == '__main__':
    app.run(debug=True)






























