#coding:utf-8
import tweepy
import sys
from neo4j.v1 import GraphDatabase,basic_auth



def getApiInstance():
	consumer_key=''
	consumer_secret=''
	access_token_key=''
	access_token_secret=''
	
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token_key,access_token_secret)

	api = tweepy.API(auth,wait_on_rate_limit = True)

	return api

def getFollowers_ids(Api,Id,Session):

	follow_ids = Api.get_user(Id)
	follow = follow_ids.name
	follow_table = str.maketrans({'\\':'\\\\','\"':'\\"',"\'":"\\'"})
	follow_name = follow.translate(follow_table)
	follow_id = follow_ids.screen_name

	# MERGE (:People{name:"",id:""})
	query = 'MERGE (:People{name:"%s",id:"%s"})' % (follow_name, follow_id)
	Session.run(query)
 
	friends_ids = tweepy.Cursor(Api.friends_ids,id = Id,cursor = -1).items()
	friends_ids_list = []

	i = 0
	try:
		for friends_id in friends_ids:
			user = Api.get_user(friends_id)
			friend_id = user.screen_name
			friend = user.name
			friend_table = str.maketrans({'\\':'\\\\','\"':'\\"',"\'":"\\'"})
			friend_name = friend.translate(friend_table)

			# MERGE (p1:People{id:""})
			# MERGE (p2:People{name:"",id:""})
			# create unique (p1)<-[:Follow]-(p2)
			query = 'MERGE (p1:People{id:"%s"})' % follow_id
			query = query + ' MERGE (p2:People{name:"%s",id:"%s"})' % (friend_name,friend_id)
			query = query + ' CREATE UNIQUE (p1)-[:Follow]->(p2)'
			session.run(query)

			i = i + 1
			if (i % 50) == 0:
				print('+50件完了')

	except tweepy.error.TweepError as e:
		print(e)

	print(i,'追加しました')



if __name__ == "__main__":
	driver = GraphDatabase.driver("bolt://localhost",auth=basic_auth("id","password"))
	session = driver.session()
	
	args = sys.argv
	if len(args) < 2:
		print("No argument")
		sys.exit()

	screen_name = args[1]

	api = getApiInstance()
	getFollowers_ids(api,screen_name,session)
	
	session.close()
