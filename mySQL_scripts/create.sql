CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE hasIllustrator(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasUsedLanguage(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id));

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasTranslator(
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasEdition(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE Edition(
	edition_id varchar (255)  primary key);

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE PlaceOfBirth(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE Translator);

CREATE TABLE hasAward(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id));

CREATE TABLE Mayor(
	mayor-id varchar (255) not null,
	end_time varchar (255),
	official_residence varchar (255) not null,
	start_time varchar (255) not null);

CREATE TABLE foundedBy(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE Book(
	subtitle varchar (255),
	book_id varchar (255)  primary key,
	title varchar (255) not null);

CREATE TABLE hasAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasRole(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE FictionalHuman);

CREATE TABLE Human(
	name varchar (255) not null,
	human_id varchar (255)  primary key,
	DoD varchar (255),
	DoB varchar (255) not null,
	sex varchar (255) not null);

CREATE TABLE locatedIn(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE Language(
	language_id varchar (255)  primary key);

CREATE TABLE FictionalNonHuman);

CREATE TABLE Character(
	character_id varchar (255)  primary key);

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Publisher(
	inception varchar (255) not null,
	publisher_id varchar (255)  primary key);

CREATE TABLE FictionalCharacter);

CREATE TABLE hasAnalog(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE hasCountry(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE Country(
	country_id varchar (255)  primary key);

CREATE TABLE hasMayor(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE City(
	city_id varchar (255)  primary key,
	description varchar (255) not null,
	label varchar (255) not null);

CREATE TABLE RealCity);

CREATE TABLE hasPublisher(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE Author);

CREATE TABLE hasAfterwordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasCharacter(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id));

CREATE TABLE BookWrittenIn(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE FictionalCity);

CREATE TABLE hasLocation(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id));

CREATE TABLE hasAuthor_Genre(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id));

CREATE TABLE PlaceOfDeath(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasForewordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

