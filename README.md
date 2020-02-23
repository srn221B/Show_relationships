## Show_relationships  
Store Twitter follow relationship in Neo4j.  

## Description  
This Program was developed to facilicate the analysis of Twitter follow relationships with neo4j.  
Save the following relatinship of the account specified in the argument.  
works on python3.  

## Demo
To see accounts on neo4j that are followed by DonaldTrump and MelaniaTrunmp.  
* run neo4j  

* run on python  
`python program.py MELANIATRUMP`  
`python program.py realDonaldTrump`  

* Executing a query  
```Cypher:sample
MATCH n=(person:People)-[:Follow]->(:People)<-[:Follow]-(person2:People)  
WHERE person.id = "MELANIATRUMP" and person2.id = "realDonaldTrump"  
return n  
```

* Can see  
![demo](https://raw.githubusercontent.com/wiki/srn221B/Show_relationships/image/mov_1.gif)  


## Usage
Python : 3.7.4  
Neo4j : 3.0.12  

* export api key  
`export twitter_consumer_key=""`  
`export twitter_consumer_secret=""`  
`export twitter_access_token_key=""`  
`export twitter_access_token_secret=""`  

* export id password on neo4j  
`export neo4j_id=""`  
`export neo4j_password=""`  

* run on python  
`python program.py <Twitter id>`  

## Author
shimoyama

