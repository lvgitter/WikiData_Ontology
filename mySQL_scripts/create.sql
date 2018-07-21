CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE foundedBy(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasCityLocation(
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE FictionalNotHuman);

CREATE TABLE hasMayor(
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasAuthor_Genre(
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Language(
	language_label varchar (255) not null,
	language_id varchar (255)  primary key,
	language_description varchar (255) not null,
	num_speakers varchar (255));

CREATE TABLE hasEdition(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Edition(
	edition_id varchar (255)  primary key,
	edition_label varchar (255) not null,
	edition_description varchar (255) not null);

CREATE TABLE Author(
	author_label varchar (255) not null,
	author_description varchar (255) not null);

CREATE TABLE Mayor(
	mayor_id varchar (255)  primary key,
	start_time varchar (255) not null,
	mayor_label varchar (255) not null,
	mayor_description varchar (255) not null,
	official_residence varchar (255) not null,
	end_time varchar (255));

CREATE TABLE BookWrittenIn(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAward(
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Translator(
	translator_label varchar (255) not null,
	translator_description varchar (255) not null);

CREATE TABLE FictionalHuman);

CREATE TABLE Book(
	book_description varchar (255) not null,
	book_label varchar (255) not null,
	book_id varchar (255)  primary key,
	title varchar (255) not null,
	subtitle varchar (255));

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE Character(
	character_description varchar (255) not null,
	character_DoD varchar (255),
	character_id varchar (255)  primary key,
	character_label varchar (255) not null,
	character_name varchar (255) not null,
	character_sex varchar (255) not null,
	character_DoB varchar (255) not null);

CREATE TABLE hasForewordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Human(
	human_description varchar (255) not null,
	human_id varchar (255)  primary key,
	sex varchar (255) not null,
	DoD varchar (255),
	human_label varchar (255) not null,
	name varchar (255) not null,
	DoB varchar (255) not null);

CREATE TABLE hasCharacter(
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE locatedIn(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE FictionalCity);

CREATE TABLE hasUsedLanguage(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE RealCity(
	area varchar (255),
	population varchar (255));

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE hasPublisher(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE hasAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Country(
	country_description varchar (255) not null,
	country_label varchar (255) not null,
	country_id varchar (255)  primary key);

CREATE TABLE Publisher(
	inception varchar (255) not null,
	publisher_description varchar (255) not null,
	publisher_id varchar (255)  primary key,
	publisher_label varchar (255) not null);

CREATE TABLE hasRole(
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasAfterwordAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE City(
	city_id varchar (255)  primary key,
	city_description varchar (255) not null,
	city_label varchar (255) not null);

CREATE TABLE FictionalCharacter);

CREATE TABLE PlaceOfDeath(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE PlaceOfBirth(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasTranslator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE hasCountry(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE hasCountryLocation(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasIllustrator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE hasAnalog(
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

