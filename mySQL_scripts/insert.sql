LOAD DATA LOCAL INFILE '../concepts/Book.txt' INTO TABLE Book
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


/*
LOAD DATA LOCAL INFILE 'hasGenre.txt' INTO TABLE Book
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
*/

LOAD DATA LOCAL INFILE '../concepts/Publisher.txt' INTO TABLE Publisher
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE '../roles/hasPublisher.txt' INTO TABLE hasPublisherBOOK
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
