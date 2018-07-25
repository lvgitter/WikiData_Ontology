DROP database bookDB;

CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE Language(
	language_id varchar (255)  primary key,
	language_label varchar (255) ,
	language_description varchar (255),
	speakers varchar (255)
	 );

CREATE TABLE influencedBy(
	author_id varchar (255),
	influencing_author_id varchar (255)
	);

CREATE TABLE hasBookGenres(
	book_id varchar (255),
	genre varchar (255)	
	);

CREATE TABLE Country(
	country_id varchar (255) primary key,
	country_label varchar (255)  ,
	country_description varchar (255),
	country_area varchar (255),
	country_population varchar (255)
	);

CREATE TABLE hasCharacter(
	book_id varchar (255),
	character_id varchar (255)
	);


CREATE TABLE locatedIn(
	publisher_id varchar (255),
	country_id varchar (255)
	);

CREATE TABLE hasCountryLocation(
	country_id varchar (255),
	book_id varchar (255)
	);

CREATE TABLE hasMayor(
	city_id varchar (255),
	mayor_id varchar (255)
	);

CREATE TABLE writtenIn(
	book_id varchar (255), 
	language_id varchar (255)
	);

CREATE TABLE hasCountry(
	city_id varchar (255),
	country_id varchar (255)
	);

CREATE TABLE FictionalCity(
	city_id varchar (255)  primary key,
	city_label varchar (255) ,
	city_description varchar (255)
	);

CREATE TABLE Mayor(
	mayor_id varchar (255)  primary key,
	mayor_label varchar (255),
	mayor_description varchar (255),
	start_time varchar (255),
	end_time varchar (255),
	official_residence varchar (255)
	);

CREATE TABLE hasForewordAuthor(
	book_id varchar (255),
	foreauthor_id varchar (255)
	);

CREATE TABLE hasAward(
	author_id varchar (255),
	award varchar (255)
	);

CREATE TABLE Charact(
	character_description varchar (255) ,
	character_DoB varchar (255) ,
	character_id varchar (255)  primary key,
	character_DoD varchar (255),
	character_name varchar (255) ,
	character_sex varchar (255) ,
	character_label varchar (255) 
	);
	

CREATE TABLE Book(
	book_id varchar (255)  primary key,
	book_label varchar (255) ,
	book_description varchar (255) ,
	title varchar (255) ,
	subtitle varchar (255),
	first_line varchar (255),
	series varchar (255)
	);

CREATE TABLE placeOfDeath(
	human_id varchar (255),
	realcity_id varchar (255)
	);

CREATE TABLE hasUsedLanguage(
	country_id varchar (255),
	language_id varchar (255)
	);

CREATE TABLE Edition(
	edition_id varchar (255)  primary key,
	edition_label varchar (255) ,
	edition_description varchar (255)
	);

CREATE TABLE foundedBy(
	publisher_id varchar (255),
	human_id varchar (255)
	);

CREATE TABLE hasIllustrator(
	edition_id varchar (255),
	human_id varchar (255)
	);

CREATE TABLE hasTranslator(
	edition_id varchar (255),
	translator_id varchar (255)
	);

CREATE TABLE hasCityLocation(
	book_id varchar (255),
	city_id varchar (255)
	);

CREATE TABLE placeOfBirth(
	human_id varchar (255),
	realcity_id varchar (255)
	);

CREATE TABLE hasAuthor(
	human_id varchar (255),
	book_id varchar (255)
	);

CREATE TABLE hasAfterwordAuthor(
	book_id varchar (255),
	afterauthor_id varchar (255)
	);

CREATE TABLE RealCity(
	city_id varchar (255)  primary key,
	city_label varchar (255) ,
	city_description varchar (255),
	realCity_area varchar (255),
	realCity_population varchar (255)
	);

CREATE TABLE hasEdition(
	book_id varchar (255),
	edition_id varchar (255)
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
	fictionalCity_id varchar (255),
	realCity_id varchar (255)
	);

CREATE TABLE FictionaNotHuman(
	character_id varchar (255) primary key,
	character_label varchar (255)  ,
	character_description varchar (255),
	character_name varchar (255),
	character_sex varchar (255),
	character_DoB varchar (255),
	character_DoD varchar (255)
	);
	
CREATE TABLE FictionaCharacter(
	character_id varchar (255) primary key,
	character_label varchar (255)  ,
	character_description varchar (255),
	character_name varchar (255),
	character_sex varchar (255),
	character_DoB varchar (255),
	character_DoD varchar (255)
	);

CREATE TABLE hasAuthorGenres(
	author_id varchar (255),
	genre varchar (255)	
	);

CREATE TABLE Publisher(
	publisher_id varchar (255)  primary key,
	publisher_label varchar (255) ,
	publisher_description varchar (255),
	inception varchar (255)
	 );

CREATE TABLE hasPublisher(
	edition_id varchar (255),
	publisher_id varchar (255)
	);


CREATE TABLE Translator(
	human_id varchar (255)  primary key,
	human_label varchar (255) ,
	human_description varchar (255) ,
	human_name varchar (255) ,
	human_sex varchar (255) ,
	human_DoB varchar (255),
	human_DoD varchar (255)
	);

CREATE TABLE speaks(
	translator_id varchar (255),
	language_id varchar (255)
	);

CREATE TABLE City(
	city_id varchar (255)  primary key,
	city_label varchar (255) ,
	city_description varchar (255) );


CREATE TABLE FictionalCharacter(
	character_id varchar (255)  primary key,
	character_label varchar (255),
	character_description varchar (255) ,
	character_name varchar (255) ,
	character_sex varchar (255) ,
	character_DoB varchar (255) ,
	character_DoD varchar (255)	
	);

CREATE TABLE FictionalHuman(
	character_id varchar (255)  primary key,
	character_label varchar (255),
	character_description varchar (255) ,
	character_name varchar (255) ,
	character_sex varchar (255) ,
	character_DoB varchar (255) ,
	character_DoD varchar (255)	
	);
	
CREATE TABLE FictionalNotHuman(
	character_id varchar (255)  primary key,
	character_label varchar (255),
	character_description varchar (255) ,
	character_name varchar (255) ,
	character_sex varchar (255) ,
	character_DoB varchar (255) ,
	character_DoD varchar (255)	
	);

CREATE TABLE hasRole(
	human_id varchar (255),
	mayor_id varchar (255)
	);

CREATE TABLE follows(
	book_id varchar (255),
	followed_book_id varchar (255)
	);

CREATE TABLE Human(
	human_id varchar (255)  primary key,
	human_label varchar (255) ,
	human_description varchar (255) ,
	human_name varchar (255) ,
	human_sex varchar (255) ,
	human_DoB varchar (255),
	human_DoD varchar (255),
	is_character varchar (255)
	 );

CREATE TABLE hasHumanOccupation(
	human_id varchar (255),
	occupation varchar (255)	
	);




