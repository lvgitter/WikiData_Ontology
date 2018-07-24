CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE Language(
	language_id varchar (255)  primary key,
	language_label varchar (255) ,
	language_description varchar (255),
	speakers varchar (255)
	 );

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE Country(
	country_id varchar (255) primary key,
	country_label varchar (255)  ,
	country_description varchar (255),
	area varchar (255),
	population varchar (255)
	);

CREATE TABLE hasCharacter(
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE FictionalHuman);

CREATE TABLE locatedIn(
	publisher_id varchar (255),
	foreign key (publisher_id) references Publisher(publisher_id),
	country_id varchar (255),
	foreign key (country_id) references Country(country_id),
	);

CREATE TABLE hasCountryLocation(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasMayor(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE writtenIn(
book_id varchar (255),
	foreign key (book_id) references Book(book_id),
	language_id varchar (255),
	foreign key (language_id) references Language(language_id)
	);

CREATE TABLE hasCountry(
	city_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realCity_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE FictionalCity(
	city_id varchar (255)  primary key,
	city_label varchar (255) ,
	city_description varchar (255)
	);

CREATE TABLE Mayor(
	mayor_description varchar (255) ,
	start_time varchar (255) ,
	official_residence varchar (255) ,
	end_time varchar (255),
	mayor_id varchar (255)  primary key,
	mayor_label varchar (255) );

CREATE TABLE hasForewordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAward(
	award_id varchar (255),
	foreign key (award_id) references Award(award_id),
	author_id varchar (255),
	foreign key (author_id) references Author(author_id));

CREATE TABLE Character(
	character_description varchar (255) ,
	character_DoB varchar (255) ,
	character_id varchar (255)  primary key,
	character_DoD varchar (255),
	character_name varchar (255) ,
	character_sex varchar (255) ,
	character_label varchar (255) );

book_id;book_label;book_description;title;subtitle;first_line;series


CREATE TABLE Book(
	book_id varchar (255)  primary key,
	book_label varchar (255) ,
	book_description varchar (255) ,
	title varchar (255) ,
	subtitle varchar (255),
	first_line varchar (255),
	series varchar (255)
	);

CREATE TABLE PlaceOfDeath(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasUsedLanguage(
	country_id varchar (255),
	foreign key (country_id) references Country(country_id),
	language_id varchar (255),
	foreign key (language_id) references Language(language_id),
	);

CREATE TABLE Edition(
	edition_id varchar (255)  primary key,
	edition_label varchar (255) ,
	edition_description varchar (255)
	);

CREATE TABLE foundedBy(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE hasIllustrator(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasTranslator(
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasCityLocation(
	city_id varchar (255),
	foreign key (city_id) references City(city_id),
	book_id varchar (255),
	foreign key (book_id) references Book(book_id));

CREATE TABLE PlaceOfBirth(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasAuthor(
	human_id varchar (255),
	foreign key (human_id) references Author(human_id),
	book_id varchar (255),
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAfterwordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE RealCity(
	city_id varchar (255)  primary key,
	city_label varchar (255) ,
	city_description varchar (255),
	realCity_area varchar (255),
	realCity_population varchar (255));

CREATE TABLE hasEdition(
	ook_id varchar (255),
	foreign key (book_id) references Book(book_id)
	edition_id varchar (255),
	foreign key (edition_id) references Edition(edition_id)	
	);


CREATE TABLE Author(
	human_id varchar (255)  primary key,
	human_label varchar (255) ,
	human_description varchar (255) ,
	human_name varchar (255) ,
	human_sex varchar (255) ,
	human_DoB varchar (255) ,
	human_DoD varchar (255)
	);

CREATE TABLE hasAnalog(
	realCity_id varchar (255),
	foreign key (realCity_id) references RealCity(realCity_id),
	fictionalCity_id varchar (255),
	foreign key (fictionalCity_id) references FictionalCity(fictionalCity_id));

CREATE TABLE FictionalNotHuman);

CREATE TABLE hasAuthor_Genre(
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Award(
	award_id varchar (255)  primary key);


CREATE TABLE Publisher(
	publisher_id varchar (255)  primary key,
	publisher_label varchar (255) ,
	publisher_description varchar (255),
	inception varchar (255)
	 );

CREATE TABLE hasPublisher(
	edition_id varchar (255),
	foreign key (edition_id) references Edition(edition_id),
	publisher_id varchar (255),
	foreign key (publisher_id) references Publisher(publisher_id)
	);

CREATE TABLE Translator(
	human_label varchar (255) ,
	human_id varchar (255)  primary key,
	sex varchar (255) ,
	DoD varchar (255),
	human_description varchar (255) ,
	name varchar (255) ,
	DoB varchar (255) );

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE City(
	city_id varchar (255)  primary key,
	city_label varchar (255) ,
	city_description varchar (255) );

CREATE TABLE FictionalCharacter(
	character_description varchar (255) ,
	character_DoB varchar (255) ,
	character_id varchar (255)  primary key,
	character_DoD varchar (255),
	character_name varchar (255) ,
	character_sex varchar (255) ,
	character_label varchar (255) );

CREATE TABLE hasRole(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Human(
	human_label varchar (255) ,
	human_id varchar (255)  primary key,
	sex varchar (255) ,
	DoD varchar (255),
	human_description varchar (255) ,
	name varchar (255) ,
	DoB varchar (255) );

