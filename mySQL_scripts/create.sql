CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Book(
	book_id varchar (255)  primary key,
	book_description varchar (255) not null,
	title varchar (255) not null,
	subtitle varchar (255),
	book_label varchar (255) not null);

CREATE TABLE FictionalCity);

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE Mayor(
	mayor_label varchar (255) not null,
	end_time varchar (255),
	official_residence varchar (255) not null,
	mayor_description varchar (255) not null,
	start_time varchar (255) not null,
	mayor_id varchar (255)  primary key);

CREATE TABLE Author(
	sex varchar (255) not null,
	human_id varchar (255)  primary key,
	human_label varchar (255) not null,
	human_description varchar (255) not null,
	DoD varchar (255),
	name varchar (255) not null,
	DoB varchar (255) not null);

CREATE TABLE Language(
	language_id varchar (255)  primary key,
	num_speakers varchar (255),
	language_description varchar (255) not null,
	language_label varchar (255) not null);

CREATE TABLE hasCityLocation(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id));

CREATE TABLE hasCharacter(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id));

CREATE TABLE hasEdition(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE Translator(
	sex varchar (255) not null,
	human_id varchar (255)  primary key,
	human_label varchar (255) not null,
	human_description varchar (255) not null,
	DoD varchar (255),
	name varchar (255) not null,
	DoB varchar (255) not null);

CREATE TABLE hasTranslator(
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasForewordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasCountry(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE PlaceOfBirth(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

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

CREATE TABLE BookWrittenIn(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id));

CREATE TABLE locatedIn(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE FictionalHuman);

CREATE TABLE Country(
	country_id varchar (255)  primary key,
	country_label varchar (255) not null,
	country_description varchar (255) not null);

CREATE TABLE FictionalCharacter(
	character_DoD varchar (255),
	character_name varchar (255) not null,
	character_label varchar (255) not null,
	character_id varchar (255)  primary key,
	character_description varchar (255) not null,
	character_sex varchar (255) not null,
	character_DoB varchar (255) not null);

CREATE TABLE PlaceOfDeath(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasRole(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE Publisher(
	publisher_id varchar (255)  primary key,
	inception varchar (255) not null,
	publisher_description varchar (255) not null,
	publisher_label varchar (255) not null);

CREATE TABLE Edition(
	edition_description varchar (255) not null,
	edition_label varchar (255) not null,
	edition_id varchar (255)  primary key);

CREATE TABLE hasAnalog(
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE City(
	city_label varchar (255) not null,
	city_id varchar (255)  primary key,
	city_description varchar (255) not null);

CREATE TABLE Character(
	character_DoD varchar (255),
	character_name varchar (255) not null,
	character_label varchar (255) not null,
	character_id varchar (255)  primary key,
	character_description varchar (255) not null,
	character_sex varchar (255) not null,
	character_DoB varchar (255) not null);

CREATE TABLE hasAfterwordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasAward(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id));

CREATE TABLE hasPublisher(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE hasMayor(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE hasAuthor_Genre(
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasCountryLocation(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE RealCity(
	population varchar (255),
	area varchar (255));

CREATE TABLE hasAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE Human(
	sex varchar (255) not null,
	human_id varchar (255)  primary key,
	human_label varchar (255) not null,
	human_description varchar (255) not null,
	DoD varchar (255),
	name varchar (255) not null,
	DoB varchar (255) not null);

CREATE TABLE FictionalNotHuman);

CREATE TABLE foundedBy(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

