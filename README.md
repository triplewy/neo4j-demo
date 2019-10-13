# Neo4j Lab

Queries:
- LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/articles.csv" AS row FIELDTERMINATOR ";" CREATE (:Article {id: row.id, title: row.title, year: row.year, conference: row.conference});

- LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/authors.csv" AS row FIELDTERMINATOR ";" CREATE (:Author {id: row.id, name: row.name});


- CREATE INDEX ON :Article(id);

- CREATE INDEX ON :Author(id);

- LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/authorsToArticles.csv" AS row FIELDTERMINATOR ';' MATCH (article:Article {id: row.paperId}) MATCH (author:Author {id: row.authorId}) MERGE (author)-[:AUTHORED]->(article);

- LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/related.csv" AS row FIELDTERMINATOR ';' MATCH (article1:Article {id: row.articleId}) MATCH (article2:Article {id: row.relatedId}) MERGE (article1)-[:CITED]->(article2);

- USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM "https://github.com/triplewy/neo4j-demo/raw/master/twitter.csv" AS row FIELDTERMINATOR " " CREATE (:User {id: row.user1}) CREATE (:User {id: row.user2});
