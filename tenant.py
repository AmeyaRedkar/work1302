from pymongo import MongoClient
from flask import Flask,request,jsonify


app=Flask(__name__)

mongohost="localhost"

mongoport=27017

client=MongoClient(mongohost,int(mongoport))

db=client["userdb"]
collection=db["users"]

@app.route('/tenants/add_tenant',methods=['POST'])
def add_tenant():
	tenant_name=request.json['tenant_name'] 
	trm=request.json['tenant_relationship_manager']
	contact=request.json['trm_contact']
	email=request.json['trm_email']
	description=request.json['tenant_description']
	creation_date=request.json['tenant_creation_date']

	try:
		data={"_id":tenant_name,"tenant_relationship_manager":trm,
		"trm_contact":contact,"trm_email":email,
		"tenant_description":description,"tenant_creation_date":creation_date
		}

		collection.insert(data)

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"403","message":"Not Created"}),403

@app.route('/tenants/delete_tenant',methods=['POST'])
def delete_tenant():
	listtenant=request.json["tenants_list"]

	
	try:
		for x in listtenant:

			collection.delete_one({"_id":x})

			return jsonify({"status":"success"}),200

	except:

		return jsonify({"status":"Failure","error code":"403","message":"Not Created"}),403

@app.route('/tenants/get_tenant',methods=['POST'])
def tenant():
	name=request.json['tenant_name']

	try:
		search=collection.find({"_id":name})
		for x in search:
			return jsonify(x),201

	except:
		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404

@app.route('/tenants/getall',methods=['GET'])
def tenants():
	search=collection.find()
	try:
		list1=[]
		for x in search:
			list1.append(x)
		
		return jsonify(list1),201

	except:
		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404



if __name__=="__main__":
	app.run(port=5000,debug=True)