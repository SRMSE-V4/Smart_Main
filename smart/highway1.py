#highway from a to b --
#highway between a and b --
#length of highway nha -- 
#highway nha length --
#highway nha route -- 
#route of highway nha -- 
#highway nha -- 
#length of highway nha in state --
#highway nha length in state -- 
#highway length nha through state --
#length of highway nha through state --
#highway which includes city --
#highway which passes over city --
#highway which passes through city --
#highway which touches city --
def highwaymod(query):
	def find_city_include(city):
		data=list(collection.find({"route":{"$in":[str(city)]}}))
		if data:
			return [{"highway":{"ans":map(removeID,data)}}]
		else:
			return "<NA>"
	def state_length(name,state):
		data=collection.find_one({"highway":str(name)})
		data1=str(data["length_state"])
		r=data1.find(state)
		if(r!=-1):
			data1=data1[int(r):]
			data1=data1.split(" (",1)
			data1=data1[1]
			data1=data1.split(")",1)
			data1=str(data1[0])
			d=[{"general":{"highway":str(name),"state":str(state),"length_state":str(data1)}}]
		else:
			#print "Highway not present in the state"
			d="<NA>"
		return d	
	#def routefind(name):
	#	try:
	#		data=collection.find({"highway":str(name)})
	#		d=[{"general":{"highway":str(name),"route":data[0]["route"]}}]
	#	except:	
	#		d="<NA>"
	#	return d
	def highwayfind(source,dest):
		try:
			data=collection.find({"route":{"$all":[str(source),str(dest)]}})
			ans=show_details(str(data[0]["highway"]))
		except:
			ans="<NA>"
		return [{"highway":{"ans":map(removeID,ans)}}]
	def calc_length(name):
		try:
			data=collection.find({"highway":str(name)})
			d=[{"general":{"length_total":data[0]["length_total"],"highway":name}}]
		except:
			d="<NA>"
		return d
	def show_details(name):
		try:
			data=collection.find({"highway":name})
			d=[{"highway":{"ans":data[0]}}]
		except:
			d="<NA>"
		return d
	from pymongo import MongoClient
	import re
	client = MongoClient()
	db=client['kbmain']
	collection=db['highways']
	if("highway" in query):
		arr=["highway","highways","from","between","to","and","which","touches"]
		for a in range(0,len(arr)):
			if(arr[a] in query):
				query=query.replace(arr[a],"")
		if("nh" in query):
			#if("route" in query):
			#	var=re.search(r'nh\w+',query)
			#	query=str(var.group())
			#	ans=routefind(query)
			if("length" in query):
				query=query.replace("length","")
				v=re.search(r'nh\w+',query)
				name=str(v.group())
				var1=re.search(r'(\w+\s*)+\w*',query)
				query=str(var1.group(1))
				var=re.search(r'nh\w+',query)
				if var:
					query=str(var.group())
					ans=calc_length(query)
				else:
					state=str(query)
					ans=state_length(name,state)
			else:
				var=re.search(r'nh\w+',query)
				query=str(var.group())
				ans=show_details(query)
		else:
			vd=re.search(r'\s\w*\s\s\w*',query)
			if vd:
				query=query.split()
				query=" ".join(query)
				query=query.split(" ",1)
				source=str(query[0])
				dest=str(query[1])
				ans=highwayfind(source,dest)
			else:
				query=query.rsplit(" ",1)
				query=str(query[1])
				ans=find_city_include(query)
	else:
		ans="<NA>"
	#print ans
	return ans


def removeID(k):
	k.pop("_id")
	return k
