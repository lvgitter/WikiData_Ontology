LOAD DATA LOCAL INFILE '../concepts/Author.txt' INTO TABLE Author
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @human_label, @human_description, @human_name, @human_sex, @human_DoB, @human_DoD)
SET human_id = IF(@human_id='',NULL,@human_id), human_label = IF(@human_label='',NULL,@human_label), human_description = IF(@human_description='',NULL,@human_description), human_name = IF(@human_name='',NULL,@human_name), human_sex = IF(@human_sex='',NULL,@human_sex), human_DoB = IF(@human_DoB='',NULL,@human_DoB), human_DoD = IF(@human_DoD='',NULL,@human_DoD);

LOAD DATA LOCAL INFILE '../concepts/Book.txt' INTO TABLE Book
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @book_label, @book_description, @title, @subtitle, @first_line, @series)
SET book_id = IF(@book_id='',null,@book_id), book_label = IF(@book_label='',null,@book_label), book_description = IF(@book_description='',null,@book_description), title = IF(@title='',null,@title), subtitle = IF(@subtitle='',null,@subtitle), first_line = IF(@first_line='',null,@first_line), series = IF(@series='',null,@series);

LOAD DATA LOCAL INFILE '../concepts/Country.txt' INTO TABLE Country
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@country_id, @country_label, @country_description, @country_area, @country_population)
SET country_id = IF(@country_id='',NULL,@country_id), country_label = IF(@country_label='',NULL,@country_label), country_description = IF(@country_description='',NULL,@country_description), country_area = IF(@country_area='',NULL,@country_area), country_population = IF(@country_population='',NULL,@country_population);

LOAD DATA LOCAL INFILE '../concepts/Edition.txt' INTO TABLE Edition
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@edition_id, @edition_label, @edition_description)
SET edition_id = IF(@edition_id='',NULL,@edition_id), edition_label = IF(@edition_label='',NULL,@edition_label), edition_description = IF(@edition_description='',NULL,@edition_description);


LOAD DATA LOCAL INFILE '../concepts/FictionalCity.txt' INTO TABLE FictionalCity
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@city_id, @city_label, @city_description)
SET city_id = IF(@city_id='',NULL,@city_id), city_label = IF(@city_label='',NULL,@city_label), city_description = IF(@city_description='',NULL,@city_description);


LOAD DATA LOCAL INFILE '../concepts/FictionalHuman.txt' INTO TABLE FictionalHuman
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@character_description, @character_DoB, @character_id, @character_DoD, @character_name, @character_sex, @character_label)
SET character_description = IF(@character_description='',NULL,@character_description), character_DoB = IF(@character_DoB='',NULL,@character_DoB), character_id = IF(@character_id='',NULL,@character_id), character_DoD = IF(@character_DoD='',NULL,@character_DoD), character_name = IF(@character_name='',NULL,@character_name), character_sex = IF(@character_sex='',NULL,@character_sex), character_label = IF(@character_label='',NULL,@character_label);

LOAD DATA LOCAL INFILE '../concepts/FictionalNotHuman.txt' INTO TABLE FictionalNotHuman
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@character_id, @character_label, @character_description, @character_name, @character_sex, @character_DoB, @character_DoD)
SET character_id = IF(@character_id='',NULL,@character_id), character_label = IF(@character_label='',NULL,@character_label), character_description = IF(@character_description='',NULL,@character_description), character_name = IF(@character_name='',NULL,@character_name), character_sex = IF(@character_sex='',NULL,@character_sex), character_DoB = IF(@character_DoB='',NULL,@character_DoB), character_DoD = IF(@character_DoD='',NULL,@character_DoD);

LOAD DATA LOCAL INFILE '../concepts/Human.txt' INTO TABLE Human
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @human_label, @human_description, @human_name, @human_sex, @human_DoB, @human_DoD, @is_character)
SET human_id = IF(@human_id='',NULL,@human_id), human_label = IF(@human_label='',NULL,@human_label), human_description = IF(@human_description='',NULL,@human_description), human_name = IF(@human_name='',NULL,@human_name), human_sex = IF(@human_sex='',NULL,@human_sex), human_DoB = IF(@human_DoB='',NULL,@human_DoB), human_DoD = IF(@human_DoD='',NULL,@human_DoD), is_character = IF(@is_character='',NULL,@is_character);

LOAD DATA LOCAL INFILE '../concepts/Language.txt' INTO TABLE Language
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@language_id, @language_label, @language_description, @speakers)
SET language_id = IF(@language_id='',NULL,@language_id), language_label = IF(@language_label='',NULL,@language_label), language_description = IF(@language_description='',NULL,@language_description), speakers = IF(@speakers='',NULL,@speakers);

LOAD DATA LOCAL INFILE '../concepts/Mayor.txt' INTO TABLE Mayor
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@mayor_id, @mayor_label, @mayor_description, @start_time, @end_time, @official_residence)
SET mayor_id = IF(@mayor_id='',NULL,@mayor_id), mayor_label = IF(@mayor_label='',NULL,@mayor_label), mayor_description = IF(@mayor_description='',NULL,@mayor_description), start_time = IF(@start_time='',NULL,@start_time), end_time = IF(@end_time='',NULL,@end_time), official_residence = IF(@official_residence='',NULL,@official_residence);

LOAD DATA LOCAL INFILE '../concepts/Publisher.txt' INTO TABLE Publisher
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@publisher_id, @publisher_label, @publisher_description, @inception)
SET publisher_id = IF(@publisher_id='',NULL,@publisher_id), publisher_label = IF(@publisher_label='',NULL,@publisher_label), publisher_description = IF(@publisher_description='',NULL,@publisher_description), inception = IF(@inception='',NULL,@inception);

LOAD DATA LOCAL INFILE '../concepts/RealCity.txt' INTO TABLE RealCity
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@city_id, @city_label, @city_description, @realCity_area, @realCity_population)
SET city_id = IF(@city_id='',NULL,@city_id), city_label = IF(@city_label='',NULL,@city_label), city_description = IF(@city_description='',NULL,@city_description), realCity_area = IF(@realCity_area='',NULL,@realCity_area), realCity_population = IF(@realCity_population='',NULL,@realCity_population);

LOAD DATA LOCAL INFILE '../concepts/Translator.txt' INTO TABLE Translator
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @human_label, @human_description, @human_name, @human_sex, @human_DoB, @human_DoD)
SET human_id = IF(@human_id='',NULL,@human_id), human_label = IF(@human_label='',NULL,@human_label), human_description = IF(@human_description='',NULL,@human_description), human_name = IF(@human_name='',NULL,@human_name), human_sex = IF(@human_sex='',NULL,@human_sex), human_DoB = IF(@human_DoB='',NULL,@human_DoB), human_DoD = IF(@human_DoD='',NULL,@human_DoD);

LOAD DATA LOCAL INFILE '../roles/foundedBy.txt' INTO TABLE foundedBy
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@publisher_id, @human_id)
SET publisher_id = IF(@publisher_id='',NULL,@publisher_id), human_id = IF(@human_id='',NULL,@human_id);

LOAD DATA LOCAL INFILE '../roles/hasAuthor.txt' INTO TABLE hasAuthor
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @book_id)
SET human_id = IF(@human_id='',NULL,@human_id), book_id = IF(@book_id='',NULL,@book_id);

LOAD DATA LOCAL INFILE '../roles/hasAfterwordAuthor.txt' INTO TABLE hasAfterwordAuthor
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @afterauthor_id)
SET book_id = IF(@book_id='',NULL,@book_id), afterauthor_id = IF(@afterauthor_id='',NULL,@afterauthor_id);

LOAD DATA LOCAL INFILE '../roles/hasAuthorGenres.txt' INTO TABLE hasAuthorGenres
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@author_id, @genre)
SET author_id = IF(@author_id='',NULL,@author_id), genre = IF(@genre='',NULL,@genre);



LOAD DATA LOCAL INFILE '../roles/hasCharacter.txt' INTO TABLE hasCharacter
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @character_id)
SET book_id = IF(@book_id='',NULL,@book_id), character_id = IF(@character_id='',NULL,@character_id);


LOAD DATA LOCAL INFILE '../roles/hasCityLocation.txt' INTO TABLE hasCityLocation
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @city_id)
SET book_id = IF(@book_id='',NULL,@book_id), city_id = IF(@city_id='',NULL,@city_id);

LOAD DATA LOCAL INFILE '../roles/hasCountry.txt' INTO TABLE hasCountry
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@city_id, @country_id)
SET city_id = IF(@city_id='',NULL,@city_id), country_id = IF(@country_id='',NULL,@country_id);

LOAD DATA LOCAL INFILE '../roles/hasCountryLocation.txt' INTO TABLE hasCountryLocation
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@country_id, @book_id)
SET country_id = IF(@country_id='',NULL,@country_id), book_id = IF(@book_id='',NULL,@book_id);

LOAD DATA LOCAL INFILE '../roles/hasIllustrator.txt' INTO TABLE hasIllustrator
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@edition_id, @human_id)
SET edition_id = IF(@edition_id='',NULL,@edition_id), human_id = IF(@human_id='',NULL,@human_id);



LOAD DATA LOCAL INFILE '../roles/hasForewordAuthor.txt' INTO TABLE hasForewordAuthor
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @foreauthor_id)
SET book_id = IF(@book_id='',NULL,@book_id), foreauthor_id = IF(@foreauthor_id='',NULL,@foreauthor_id);

LOAD DATA LOCAL INFILE '../roles/hasTranslator.txt' INTO TABLE hasTranslator
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@edition_id, @translator_id)
SET edition_id = IF(@edition_id='',NULL,@edition_id), translator_id = IF(@translator_id='',NULL,@translator_id);

LOAD DATA LOCAL INFILE '../roles/hasUsedLanguage.txt' INTO TABLE hasUsedLanguage
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@country_id, @language_id)
SET country_id = IF(@country_id='',NULL,@country_id), language_id = IF(@language_id='',NULL,@language_id);

LOAD DATA LOCAL INFILE '../roles/hasMayor.txt' INTO TABLE hasMayor
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@city_id, @mayor_id)
SET city_id = IF(@city_id='',NULL,@city_id), mayor_id = IF(@mayor_id='',NULL,@mayor_id);

LOAD DATA LOCAL INFILE '../roles/hasPublisher.txt' INTO TABLE hasPublisher
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@edition_id, @publisher_id)
SET edition_id = IF(@edition_id='',NULL,@edition_id), publisher_id = IF(@publisher_id='',NULL,@publisher_id);

LOAD DATA LOCAL INFILE '../roles/influencedBy.txt' INTO TABLE influencedBy
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@author_id, @influencing_author_id)
SET author_id = IF(@author_id='',NULL,@author_id), influencing_author_id = IF(@influencing_author_id='',NULL,@influencing_author_id);

LOAD DATA LOCAL INFILE '../roles/locatedIn.txt' INTO TABLE locatedIn
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@publisher_id, @country_id)
SET publisher_id = IF(@publisher_id='',NULL,@publisher_id), country_id = IF(@country_id='',NULL,@country_id);

LOAD DATA LOCAL INFILE '../roles/placeOfBirth.txt' INTO TABLE placeOfBirth
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @realcity_id)
SET human_id = IF(@human_id='',NULL,@human_id), realcity_id = IF(@realcity_id='',NULL,@realcity_id);

LOAD DATA LOCAL INFILE '../roles/placeOfDeath.txt' INTO TABLE placeOfDeath
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @realcity_id)
SET human_id = IF(@human_id='',NULL,@human_id), realcity_id = IF(@realcity_id='',NULL,@realcity_id);


LOAD DATA LOCAL INFILE '../roles/writtenIn.txt' INTO TABLE writtenIn
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @language_id)
SET book_id = IF(@book_id='',NULL,@book_id), language_id = IF(@language_id='',NULL,@language_id);


LOAD DATA LOCAL INFILE '../roles/hasEdition.txt' INTO TABLE hasEdition
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @edition_id)
SET book_id = IF(@book_id='',NULL,@book_id), edition_id = IF(@edition_id='',NULL,@edition_id);


LOAD DATA LOCAL INFILE '../roles/hasAnalog.txt' INTO TABLE hasAnalog
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@fictionalCity_id, @realCity_id)
SET fictionalCity_id = IF(@fictionalCity_id='',NULL,@fictionalCity_id), realCity_id = IF(@realCity_id='',NULL,@realCity_id);

LOAD DATA LOCAL INFILE '../roles/hasAuthorAwards.txt' INTO TABLE hasAward
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@author_id, @award)
SET author_id = IF(@author_id='',NULL,@author_id), award = IF(@award='',NULL,@award);


LOAD DATA LOCAL INFILE '../roles/hasBookGenres.txt' INTO TABLE hasBookGenres
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @genre)
SET book_id = IF(@book_id='',NULL,@book_id), genre = IF(@genre='',NULL,@genre);

LOAD DATA LOCAL INFILE '../roles/hasHumanOccupation.txt' INTO TABLE hasHumanOccupation
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @occupation)
SET human_id = IF(@human_id='',NULL,@human_id), occupation = IF(@occupation='',NULL,@occupation);


LOAD DATA LOCAL INFILE '../roles/speaks.txt' INTO TABLE speaks
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@translator_id, @language_id)
SET translator_id = IF(@translator_id='',NULL,@translator_id), language_id = IF(@language_id='',NULL,@language_id);

LOAD DATA LOCAL INFILE '../roles/hasRole.txt' INTO TABLE hasRole
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@human_id, @mayor_id)
SET human_id = IF(@human_id='',NULL,@human_id), mayor_id = IF(@mayor_id='',NULL,@mayor_id);

LOAD DATA LOCAL INFILE '../roles/follows.txt' INTO TABLE follows
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@book_id, @followed_book_id)
SET book_id = IF(@book_id='',NULL,@book_id), followed_book_id = IF(@followed_book_id='',NULL,@followed_book_id);



