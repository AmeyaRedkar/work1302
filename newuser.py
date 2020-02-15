from pymongo import MongoClient
from flask import Flask,request,jsonify


app=Flask(__name__)

mongohost="enter url"

mongoport="enter port" #27017

client=MongoClient(mongohost,int(mongoport))

db=client["userdb"]
collection=db["users"]

@app.route('/users/changepassword',methods=['POST'])
def changepassword():
	username=request.json['username'] 
	newpassword=request.json['new_password']

	try:

		collection.update_one({"_id":username},{"$set":{"password":newpassword}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404


@app.route('/users/changeprivilege',methods=['POST'])
def changeprivilege():
	username=request.json['username'] 
	newprivilege=request.json['new_privilege_level']

	try:

		collection.update_one({"_id":username},{"$set":{"privilege":newprivilege}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404


@app.route('/users/updatetenantlist',methods=['POST'])
def updatetenanat():
	username=request.json['username'] 
	newtentantlist=request.json['tenant_list']

	try:

		collection.update_one({"_id":username},{"$set":{"tenants_list":newtentantlist}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404

@app.route('/users/change_active_tenant',methods=['POST'])
def activetentant():
	username=request.json['username'] 
	tentant=request.json['tenant_name']

	try:
		
		collection.update_one({"_id":username},{"$set":{"last_accessed_tenant":tentant}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404


@app.route('/users/getuserfortenant',methods=['POST'])
def getuserfortennant():

	tenants_list=request.json['tenant_list']
	
	try:
		search=collection.find()
		list1=[]
			for x in search:
				list1.append(x)

		l1=[]
		l2=[]
		
		for tenant in tenants_list:
			for users in search:
				if user["privilege"]==1 and user["tenants_list"]==tenant:
					l1.append(tenant)

				elif user["privilege"]==2 and user["tenants_list"]==tenant:
					l2.append(tenant)

			collection.insert({tenant:{"l1_users":l1,"l2_users" :l2}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404



if __name__=="__main__":
	app.run(port=5000,debug=True)
