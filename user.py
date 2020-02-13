from pymongo import MongoClient
from flask import Flask,request,jsonify


app=Flask(__name__)

mongohost="enter url"

mongoport="enter port" #27017

client=MongoClient(mongohost,int(mongoport))

db=client["userdb"]
collection=db["users"]


@app.route('/users/adduser',methods=['POST'])
def adduser():
	username=request.json['username'] 
	password=request.json['password']
	privilege=request.json['privilege']
	tenlist=request.json['tenants']
	
	try:
		userentry={"_id":username,"password":password,"privilege":privilege,"tenants_list":tenlist}
		collection.insert(userentry)
		
		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"403","message":"Not Created"}),403


@app.route('/users/deleteuser',methods=['POST'])
def deleteuser():
	username=request.json['users']

	
	try:
		for x in username:
			collection.delete_one({"_id":x})

		return jsonify({"status":"success"}),200

	except:

		return jsonify({"status":"Failure","error code":"403","message":"Not Created"}),403


@app.route('/users/changepassword',methods=['POST'])
def changepassword():
	username=request.json['username'] 
	#oldpassword=request.json['old_password']   if old password is required to change
	newpassword=request.json['new_password']

	try:

	#search=collection.find({"$and":[{"_id":username,"password":oldpassword}]})
	# list1=[x for x in search] 
	#lambda used to reduce code but as you told not to use so elaborated one is in down
	
		search=collection.find({"_id":username})

		list1=[]
		for x in search:
			list1.append(x)

		#for match in list1:
		#	if match["_id"]==username and match["password"]==oldpassword:
		#		collection.update_one({"password":oldpassword},{"$set":{"password":newpassword}})
		
		for match in list1:
			if match["_id"]==username:
				collection.update_one({"password":match["password"]},{"$set":{"password":newpassword}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404

	

@app.route('/users/changeprivilege',methods=['POST'])
def changeprivilege():
	username=request.json['username'] 
	newprivilege=request.json['new_privilege_level']

	try:

		search=collection.find({"_id":username})

		list1=[]
		for x in search:
			list1.append(x)

		for match in list1:
			if match["_id"]==username:
				collection.update_one({"privilege":match["privilege"]},{"$set":{"privilege":newprivilege}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404

	

@app.route('/users/updatetenantlist',methods=['POST'])
def updatetenanat():
	username=request.json['username'] 
	newtentantlist=request.json['tenant_list']

	try:
		search=collection.find({"_id":username})

		list1=[]
		for x in search:
			list1.append(x)

		for match in list1:
			if match["_id"]==username:
				collection.update_one({"tenants_list":match["tenants_list"]},{"$set":{"tenants_list":newtentantlist}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404

	

@app.route('/users/userinfo',methods=['POST'])
def userinfo():
	username=request.json['username']

	try:
		search=collection.find({"_id":username})

		list1=[]
		for x in search:
			list1.append(x)

		return jsonify({"userdata":list1}),201 #list is returned

	#for x in list1:
	#	return jsonify({"userdata":x})    dictionary is returned

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404


@app.route('/users/getallusers',methods=['GET'])
def getallusers():
	
	try:
		search=collection.find()
		list1=[]
		for x in search:
			list1.append(x)
	
		return jsonify({"user_data":list1}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404


@app.route('/users/change_active_tenant',methods=['POST'])
def activetentant():
	username=request.json['username'] 
	tentant=request.json['tenant_name']

	try:
		search=collection.find({"_id":username})

		list1=[]
		for x in search:
			list1.append(x)

		for match in list1:
			if match["_id"]==username:

				collection.update_one({"last_accessed_tenant":match["last_accessed_tenant"]},{"$set":{"last_accessed_tenant":tentant}})

		return jsonify({"status":"success"}),201

	except:

		return jsonify({"status":"Failure","error code":"404","message":"Data Not Found"}),404



if __name__=="__main__":
	app.run(port=5000,debug=True)


