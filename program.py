#coding:utf-8
import tweepy
import sys
import os
from neo4j.v1 import GraphDatabase,basic_auth

# APIインスタンスの生成
def getApiInstance():
	# consumer_key,consumer_secret,access_token_key,access_token_secretを環境変数から用いる
	consumer_key = os.environ['twitter_consumer_key']
	consumer_secret = os.environ['twitter_consumer_secret']
	access_token_key = os.environ['twitter_access_token_key']
	access_token_secret = os.environ['twitter_access_token_secret']
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token_key,access_token_secret)

	#　APIインスタンスを生成
	#  wait_on_rate_limit = True でAPI利用制限時に待機
	api = tweepy.API(auth,wait_on_rate_limit = True)

	# インスタンスを返却
	return api

# Neo4jへFollow情報を登録（APIインスタンス,アカウントID，Neo4jセッション）
def getFollowers_ids(Api,Id,Session):

	# 引数に指定したアカウントの情報をアカウントIDから取得
	follow_inf = Api.get_user(Id)
	# アカウント名を取得
	follow = follow_inf.name
	# 文字の置き換え（\→\\,"→\",'→\')
	follow_table = str.maketrans({'\\':'\\\\','\"':'\\"',"\'":"\\'"})
	follow_name = follow.translate(follow_table)
	# アカウントIDを取得
	follow_id = follow_inf.screen_name

	# クエリの生成　アカウントを登録
	# MERGE (:People{name:"アカウント名",id:"アカウントID"})
	query = 'MERGE (:People{name:"%s",id:"%s"})' % (follow_name, follow_id)
	Session.run(query)

	# アカウントIDからフォローしている人のID一覧を取得
	friends_ids = tweepy.Cursor(Api.friends_ids,id = Id,cursor = -1).items()

	# 件数数えるための変数
	i = 0

	try:
		for friends_id in friends_ids:
			# IDからアカウントの情報を取得
			user = Api.get_user(friends_id)
			# アカウント名を取得
			friend = user.name
			# 文字の置き換え（\→\\,"→\",'→\')
			friend_table = str.maketrans({'\\':'\\\\','\"':'\\"',"\'":"\\'"})
			friend_name = friend.translate(friend_table)
			# アカウントIDを取得
			friend_id = user.screen_name

			# クエリの作成　アカウントの登録および関係性の生成
			# MERGE (p1:Pople{id:"アカウントID"})
			# MERGE (p2:People{name:"フォロー先アカウント名",id:"フォロー先アカウントID"})
			# CREATE UNIQUE (p1)-[:Follow]->(p2)
			query = 'MERGE (p1:People{id:"%s"})' % follow_id
			query = query + ' MERGE (p2:People{name:"%s",id:"%s"})' % (friend_name,friend_id)
			query = query + ' CREATE UNIQUE (p1)-[:Follow]->(p2)'
			session.run(query)

			# ５０件ごとに表示する
			i = i + 1
			if (i % 50) == 0:
				print('+50件完了')

	except tweepy.error.TweepError as e:
		print(e)
	
	#合計追加件数を表示
	print(i,'追加しました')


# 引数取得
args = sys.argv
# プログラム実行時に引数があるか判定。ない場合は終了。ある場合は変数に格納
if len(args) < 2:
	print("引数（アカウントID）を指定してください。")
	sys.exit()
else:
	screen_name = args[1]

# Neo4jのIDを環境変数から取得
id = os.environ['neo4j_id']
# Neo4jのpasswordを環境変数から取得
password = os.environ['neo4j_password']
# Neo4jを利用するためのドライバーを準備
driver = GraphDatabase.driver("bolt://localhost",auth=basic_auth(id,password))
# Neo4jへのセッションを開始
session = driver.session()
# Tweepyを使うためのAPIインスタンス生成
api = getApiInstance()
# Neo4jへFollow情報を登録（APIインスタンス,アカウントID，Neo4jセッション）
getFollowers_ids(api,screen_name,session)
# Neo4jへのセッションの終了
session.close()
