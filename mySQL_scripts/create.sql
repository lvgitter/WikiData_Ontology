CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE hasRole(
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE FictionalCharacter);

CREATE TABLE Book(
	subtitle varchar (255),
	book_id varchar (255)  primary key,
	title varchar (255) not null);

CREATE TABLE foundedBy(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasAuthor_Genre(
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasForewordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasAward(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id));

CREATE TABLE City(
	city_id varchar (255)  primary key,
	label varchar (255) not null,
	description varchar (255) not null);

CREATE TABLE hasCharacter(
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAfterwordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE speaks(
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id),
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id));

CREATE TABLE Country(
	country_id varchar (255)  primary key);

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Character(
	character_id varchar (255)  primary key);

CREATE TABLE BookWrittenIn(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE hasCountry(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasUsedLanguage(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id));

CREATE TABLE RealCity);

CREATE TABLE hasAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Language(
	language_id varchar (255)  primary key);

CREATE TABLE Human(
	DoB varchar (255) not null,
	sex varchar (255) not null,
	name varchar (255) not null,
	human_id varchar (255)  primary key,
	DoD varchar (255));

CREATE TABLE hasMayor(
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE FictionalNonHuman);

CREATE TABLE hasAnalog(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id));

CREATE TABLE hasIllustrator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE FictionalCity);

CREATE TABLE Publisher(
	inception varchar (255) not null,
	publisher_id varchar (255)  primary key);

CREATE TABLE Translator);

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE FictionalHuman);

CREATE TABLE locatedIn(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE PlaceOfDeath(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasTranslator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE Edition(
	edition_id varchar (255)  primary key);

CREATE TABLE hasEdition(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasPublisher(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasLocation(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id));

CREATE TABLE Author);

CREATE TABLE Mayor(
	official_residence varchar (255) not null,
	mayor-id varchar (255) not null,
	end_time varchar (255),
	start_time varchar (255) not null);

CREATE TABLE PlaceOfBirth(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

