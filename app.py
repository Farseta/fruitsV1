import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, jsonify, url_for
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
   fruit = list(db.fruit.find({}))
   return render_template('dashboard.html',Fruit=fruit)

@app.route('/fruit',methods=['GET'])
def fruit():
   fruit = list(db.fruit.find({}))
   
   return render_template('fruit.html',Fruit=fruit)

@app.route('/editFruit/<_id>',methods=['GET','POST'])
def editFruit(_id):
   if request.method == 'POST':
      id = request.form["_id"]
      name = request.form['fruitsName']
      price = request.form['price']
      description = request.form['descriptionProduct']
      image = request.files['image']
      print(name,price,description)
      doc = {
         "name": name,
         "price": price,
         "description": description,
      }
      if image:
            extention = image.filename.split('.')[-1]
            today = datetime.now()
            mytime =today.strftime("%Y-%m-%d-%H-%M-%S")
            fileName =f'static/assets/imgFruit/post-{mytime}.{extention}'
            image.save(fileName)
            doc['image'] = fileName
            print(fileName)
      db.fruit.update_one({"_id":ObjectId(id)},{"$set":doc})
      return redirect(url_for('fruit'))
   id = ObjectId(_id)
   data = list(db.fruit.find({"_id":id}))
   return render_template('EditFruit.html',Data=data)

@app.route('/addFruit',methods=['GET','POST'])
def addFruit():
   if request.method =='POST':
         name = request.form['fruitsName']
         price = request.form['price']
         # for image?
         image = request.files['image']
         
         if image:
            extention = image.filename.split('.')[-1]
            today = datetime.now()
            mytime =today.strftime("%Y-%m-%d-%H-%M-%S")
            fileName =f'static/assets/imgFruit/post-{mytime}.{extention}'
            image.save(fileName)
            print(fileName)
         else:
            image = None
         # end for image?
         description = request.form['descriptionProduct']
         print(name,price,description)
         doc = {
            "name": name,
            "price": price,
            "description": description,
            "image": fileName
         }
         db.fruit.insert_one(doc)
         return redirect(url_for("fruit"))
   return render_template('AddFruit.html')

@app.route('/deleteFruit/<_id>',methods=['GET',"POST"])
def deleteFruit(_id):
   db.fruit.delete_one({"_id":ObjectId(_id)})
   
   return redirect(url_for("fruit"))

if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)