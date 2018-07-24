CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE Language(
	language_id varchar (255)  primary key,
	language_label varchar (255) ,
	language_description varchar (255),
	speakers varchar (255)
	 );

CREATE TABLE InfluencedBy(
	author_id varchar (255),
	foreign key (author_id) references Author(author_id),
	influencing_author_id varchar (255),
	foreign key (influencing_author_id) references Author(author_id),
	);

CREATE TABLE hasBookGenre(
	book_id varchar (255),
	foreign key (book_id) references Book(book_id),
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
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id)
	);


CREATE TABLE FictionalHuman(
	character_id varchar (255) primary key,
	character_label varchar (255)  ,
	character_description varchar (255),
	character_name varchar (255),
	character_sex varchar (255),
	character_DoB varchar (255),
	character_DoD varchar (255)
	);

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
	city_id varchar (255),
	foreign key (city_id) references RealCity(city_id),
	mayor_id varchar (255),
	foreign key (mayor_id) references Mayor(mayor_id)
	);

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
	mayor_id varchar (255)  primary key,
	mayor_label varchar (255),
	mayor_description varchar (255),
	start_time varchar (255),
	end_time varchar (255),
	official_residence varchar (255)
	);

CREATE TABLE hasForewordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	foreauthor_id varchar (255)  primary key,
	foreign key (foreauthor_id) references Author(author_id)	
	);

CREATE TABLE hasAward(
	author_id varchar (255),
	foreign key (author_id) references Author(author_id),
	award varchar (255)
	);

CREATE TABLE Character(
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

CREATE TABLE PlaceOfDeath(
	realcity_id varchar (255),
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255),
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
	publisher_id varchar (255),
	foreign key (publisher_id) references Publisher(publisher_id)
	human_id varchar (255),
	foreign key (human_id) references Human(human_id),
	);

CREATE TABLE hasIllustrator(
	edition_id varchar (255),
	foreign key (edition_id) references Edition(edition_id)
	human_id varchar (255),
	foreign key (human_id) references Human(human_id)	
	);

CREATE TABLE hasTranslator(
	edition_id varchar (255),
	foreign key (edition_id) references Edition(edition_id),
	translator_id varchar (255),
	foreign key (translator_id) references Translator(translator_id),
	);

CREATE TABLE hasCityLocation(
	city_id varchar (255),
	foreign key (city_id) references City(city_id),
	book_id varchar (255),
	foreign key (book_id) references Book(book_id));

CREATE TABLE PlaceOfBirth(
	realcity_id varchar (255),
	human_id varchar (255)
	);

CREATE TABLE hasAuthor(
	human_id varchar (255),
	foreign key (human_id) references Author(human_id),
	book_id varchar (255),
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAfterwordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	afterauthor_id varchar (255)  primary key,
	foreign key (afterauthor_id) references Author(author_id)
	);

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
	fictionalCity_id varchar (255),
	foreign key (fictionalCity_id) references FictionalCity(fictionalCity_id),
	realCity_id varchar (255),
	foreign key (realCity_id) references RealCity(realCity_id)	
	);

CREATE TABLE FictionaNotlHuman(
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

CREATE TABLE hasAuthorGenre(
	author_id varchar (255),
	foreign key (author_id) references Author(author_id),
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
	foreign key (edition_id) references Edition(edition_id),
	publisher_id varchar (255),
	foreign key (publisher_id) references Publisher(publisher_id)
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
	foreign key (translator_id) references Translator(translator_id))
	language_id varchar (255),
	foreign key (language_id) references Language(language_id)
	);

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
	character_label varchar (255) 
	);

CREATE TABLE hasRole(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE follows(
	book_id varchar (255),
	foreign key (book_id) references Book(book_id),
	followed_book_id varchar (255),
	foreign key (followed_book_id) references Book(book_id),
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

