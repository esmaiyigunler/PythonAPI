from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)


connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=PAPATYA\\SQLEXPRESS01;"
    "Database=books;"
    "Trusted_Connection=yes;"
)
cursor = connection.cursor()
print("SQL bağlantısı sağlandı")


@app.route('/books', methods=['GET'])
def get_books():
    cursor.execute("SELECT * FROM Books")
    Books=[{
        "bookID":row[0],
        "title":row[1],
        "author":row[2],
        "year":row[3],
        "stock":row[4]

      }
      for row in cursor.fetchall()
    ]
    return jsonify(Books)



@app.route("/books", methods=["POST"])
def post_books():
    data = request.get_json()
    cursor.execute("INSERT INTO Books (title, author, year,stock) VALUES (?, ?, ?,?)", data['title'], data['author'], data['year'], data['stock'])
    connection.commit()
    return jsonify({"message": "Kitap başarıyla eklendi"}), 201

@app.route('/books/<int:bookID>',methods=['PUT'])
def getbooks(bookID):
    data=request.get_json()
    cursor.execute("UPDATE Books SET title=?, author=?, year=?, stock=? WHERE bookID=?",data.get('title'), data.get('author'), data.get('year'), data.get("stock"),bookID)
    connection.commit()
    return jsonify({"message": "Kitap güncellendi"}), 201


@app.route('/books/<int:bookID>', methods=['DELETE'])
def delete_books(bookID):
    cursor.execute("SELECT * FROM Books WHERE bookID = ?", bookID)
    book = cursor.fetchone()
    if not book:
        return jsonify({"error": "Belirtilen ID'ye sahip kitap bulunamadı."}), 404

    cursor.execute("DELETE FROM Books WHERE bookID = ?", bookID)
    connection.commit()
    return jsonify({"message": "Kitap silindi"}), 200



if __name__ == '__main__':
    app.run(debug=True)





