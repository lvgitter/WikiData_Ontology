CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE Language(
	num_speakers varchar (255),
	language_id varchar (255)  primary key,
	language_description varchar (255) not null,
	language_label varchar (255) not null);

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE Country(
	country_label varchar (255) not null,
	country_id varchar (255)  primary key,
	country_description varchar (255) not null);

CREATE TABLE hasCharacter(
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE FictionalHuman);

CREATE TABLE locatedIn(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

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

CREATE TABLE BookWrittenIn(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasCountry(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE FictionalCity);

CREATE TABLE Mayor(
	mayor_description varchar (255) not null,
	start_time varchar (255) not null,
	official_residence varchar (255) not null,
	end_time varchar (255),
	mayor_id varchar (255)  primary key,
	mayor_label varchar (255) not null);

CREATE TABLE hasForewordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAward(
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Character(
	character_description varchar (255) not null,
	character_DoB varchar (255) not null,
	character_id varchar (255)  primary key,
	character_DoD varchar (255),
	character_name varchar (255) not null,
	character_sex varchar (255) not null,
	character_label varchar (255) not null);

CREATE TABLE Book(
	book_label varchar (255) not null,
	book_description varchar (255) not null,
	subtitle varchar (255),
	title varchar (255) not null,
	book_id varchar (255)  primary key);

CREATE TABLE PlaceOfDeath(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasUsedLanguage(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE Edition(
	edition_label varchar (255) not null,
	edition_description varchar (255) not null,
	edition_id varchar (255)  primary key);

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
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE PlaceOfBirth(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAfterwordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE RealCity(
	population varchar (255),
	area varchar (255));

CREATE TABLE hasEdition(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Author(
	human_label varchar (255) not null,
	human_id varchar (255)  primary key,
	sex varchar (255) not null,
	DoD varchar (255),
	human_description varchar (255) not null,
	name varchar (255) not null,
	DoB varchar (255) not null);

CREATE TABLE hasAnalog(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id));

CREATE TABLE FictionalNotHuman);

CREATE TABLE hasAuthor_Genre(
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE Publisher(
	publisher_label varchar (255) not null,
	inception varchar (255) not null,
	publisher_id varchar (255)  primary key,
	publisher_description varchar (255) not null);

CREATE TABLE hasPublisher(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE Translator(
	human_label varchar (255) not null,
	human_id varchar (255)  primary key,
	sex varchar (255) not null,
	DoD varchar (255),
	human_description varchar (255) not null,
	name varchar (255) not null,
	DoB varchar (255) not null);

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE City(
	city_id varchar (255)  primary key,
	city_description varchar (255) not null,
	city_label varchar (255) not null);

CREATE TABLE FictionalCharacter(
	character_description varchar (255) not null,
	character_DoB varchar (255) not null,
	character_id varchar (255)  primary key,
	character_DoD varchar (255),
	character_name varchar (255) not null,
	character_sex varchar (255) not null,
	character_label varchar (255) not null);

CREATE TABLE hasRole(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Human(
	human_label varchar (255) not null,
	human_id varchar (255)  primary key,
	sex varchar (255) not null,
	DoD varchar (255),
	human_description varchar (255) not null,
	name varchar (255) not null,
	DoB varchar (255) not null);

