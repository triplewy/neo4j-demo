# Neo4j Lab

<h2>ETL:</h2>

<h3>Citations Dataset</h3>

<pre>LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/articles.csv" AS row FIELDTERMINATOR ";" CREATE (:Article {id: row.id, title: row.title, year: row.year, conference: row.conference});</pre>

<pre>LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/authors.csv" AS row FIELDTERMINATOR ";" CREATE (:Author {id: row.id, name: row.name});</pre>

<pre>CREATE INDEX ON :Article(id);</pre>

<pre>CREATE INDEX ON :Author(id);</pre>

<pre>LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/authorsToArticles.csv" AS row FIELDTERMINATOR ';' MATCH (article:Article {id: row.paperId}) MATCH (author:Author {id: row.authorId}) MERGE (author)-[:AUTHORED]->(article);</pre>

<pre>LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/related.csv" AS row FIELDTERMINATOR ';' MATCH (article1:Article {id: row.articleId}) MATCH (article2:Article {id: row.relatedId}) MERGE (article1)-[:CITED]->(article2);</pre>

<h3>Twitter Dataset</h3>

<pre>USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/twitter_tiny.csv" AS row FIELDTERMINATOR " " CREATE (:User {id: row.id});</pre>

<pre>CREATE INDEX ON :User(id);</pre>

<pre>LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/twitter_small.csv" AS row FIELDTERMINATOR " " MATCH (user1:User {id: row.user1}) MATCH (user2:User {id: row.user2}) MERGE (user1)-[:FOLLOWS]->(user2);</pre>

<h2>Queries:</h2>

<h3>Citations Dataset</h3>

Papers with most citations
<pre>MATCH (a)-[:CITED]->(b) RETURN b, COLLECT(a) as papers ORDER BY SIZE(papers) DESC LIMIT 10;</pre>

Authors with most papers
<pre>MATCH (a)-[:AUTHORED]->(b) WHERE (a.name <> "Staff" AND a.name <> " Jr.") RETURN a, COLLECT(b) as papers ORDER BY SIZE(papers) DESC LIMIT 10;</pre>

Authors who cited their own papers
<pre>MATCH (author1)-[:AUTHORED]->(a)-[:CITED]->(b)<-[:CITED]-(c)<-[:AUTHORED]-(author2) WHERE (author1.id = author2.id) RETURN author1 LIMIT 10;</pre>


<h3>Twitter Dataset</h3>

Delete everything

<pre>MATCH (n) DETACH DELETE n;</pre>

Create users, subscriptions and medical reports for the first day

<pre>MERGE (u1:User {name: "Alex"})
MERGE (u2:User {name: "Bob"})
MERGE (u3:User {name: "Cathy"})
MERGE (u4:User {name: "David"})
MERGE (u5:User {name: "Eric"})
MERGE (u1)-[:subscribe]->(u2)
MERGE (u1)-[:subscribe]->(u3)
MERGE (u2)-[:subscribe]->(u5)
MERGE (u3)-[:subscribe]->(u4)
MERGE (u3)-[:subscribe]->(u2)
MERGE (u4)-[:subscribe]->(u1)
MERGE (u5)-[:subscribe]->(u4)
MERGE (u1)-[:report]-(:DailyMedicalRecord {affected: true, day: 1})
MERGE (u2)-[:report]-(:DailyMedicalRecord {affected: false, day: 1})
MERGE (u3)-[:report]-(:DailyMedicalRecord {affected: false, day: 1})
MERGE (u4)-[:report]-(:DailyMedicalRecord {affected: false, day: 1})
MERGE (u5)-[:report]-(:DailyMedicalRecord {affected: false, day: 1})</pre>




TODO: add recovery

If the friend-affection ratio is higher than rand() for a user, affect this user

<pre>MATCH (x:DailyMedicalRecord)
WITH MAX(x.day) as yesterday
MATCH (u: User)-[:report]-(r:DailyMedicalRecord {day: yesterday})
WITH u, r, 
    yesterday, 
    size((u)-[:subscribe]-(:User)) as total_sub, 
    size((u)-[:subscribe]-(:User)-[:report]-(:DailyMedicalRecord {affected: true, day: yesterday})) as affected_sub
WITH u, r, yesterday, affected_sub * 1.0  / total_sub as ratio
WITH u, yesterday, ratio > rand() OR r.affected as is_affected
MERGE (u)-[:report]-(new_record:DailyMedicalRecord {affected: is_affected, day: yesterday + 1})</pre>


This only work out of sandbox. In sand box, use GUI export button
<pre>CALL apoc.export.csv.query("MATCH (n) RETURN n", "records.csv", {})</pre>
