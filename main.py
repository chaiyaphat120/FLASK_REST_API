from flask import Flask,request
import sqlite3
app = Flask(__name__)
app.config['DEBUG'] = True  #nodemon
#สร้าง table ใน sqlite
# c.execute('CREATE TABLE books (author text, id next , title text, price real)')
# real คือจำนวนจริง 


#สำหรับ ดึงข้อมูลมาแสดง
books2=[
    {"title":"book1","price":299 , "id":1, "author":"admin"}
]

@app.route('/<string:username>',methods=['GET'])
#http://127.0.0.1:8080/janny
def hello(username):
    # http://127.0.0.1:8080?q=janny
    return {"message":username}, 201

#เขียนลง database แล้ว ส่ง return มาให้ client
@app.route('/book',methods=['POST',"GET","PUT","DELETE"])
def book():
    #connect sqlite
    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()

    if request.method == "POST":
        # print(request.data) # b'{\r\n    "hello":"world55"\r\n}'
        print(request.get_json())  # body
        body = request.get_json()
        c.execute('INSERT INTO books VALUES (?,?,?,?)',
        (body['author'],body['id'], body['title'],body['price'])) #add ลง sqlite
        conn.commit()  #save ลง slite
        books2.append(body)
        return{
            " message":"Book already add to database", "body":body
        }, 201
    elif request.method == "GET":
        rows = []
        for row in c.execute('SELECT * FROM books'):
            rows.append({
                "title":row[2],"price":row[3],"id":row[1],"price":row[0]
            })
        return{"Book":rows}, 200

    #PUT เอาข้อมูลใหม่แทนชุดเก่า  การแทนที่ใน database
    #PUT (body) {"titile":"book2","price":199,"id":1}
    elif request.method =="PUT":
        body = request.get_json()
        c.execute("UPDATE books SET author = ?,title = ? , price = ? WHERE id = ?",
            (body['author'], body['title'], body['price'],body['id'])
        )
        conn.commit()
        # for i, book in enumerate(books2):
        #     if book['id']==body['id']:
        #         books2[i] = body
        return {"message":"Book has been replace", "body":body}, 200
    
    elif request.method == "DELETE":
        deleteId = request.args.get('id')
        c.execute("DELETE FROM books WHERE id=?",deleteId)
        conn.commit()

        # for i,book in enumerate(books2):  #loop ใน database
        #     if book['id'] == int(deleteId):
        #         books2.pop(i)  #delete form index
        return {"message":"Book is deleted"}, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
app.run()