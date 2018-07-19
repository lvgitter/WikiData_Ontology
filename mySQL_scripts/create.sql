CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE Human(
	DoD varchar (255),
	name varchar (255) not null,
	human_description varchar (255) not null,
	human_label varchar (255) not null,
	sex varchar (255) not null,
	human_id varchar (255)  primary key,
	DoB varchar (255) not null);

CREATE TABLE RealCity(
	population varchar (255),
	area varchar (255));

CREATE TABLE hasCountryLocation(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Mayor(
	mayor_description varchar (255) not null,
	end_time varchar (255),
	official_residence varchar (255) not null,
	mayor_id varchar (255)  primary key,
	start_time varchar (255) not null,
	mayor_label varchar (255) not null);

CREATE TABLE hasPublisher(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE Publisher(
	publisher_label varchar (255) not null,
	publisher_id varchar (255)  primary key,
	publisher_description varchar (255) not null,
	inception varchar (255) not null);

CREATE TABLE hasTranslator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE Country(
	country_description varchar (255) not null,
	country_label varchar (255) not null,
	country_id varchar (255)  primary key);

CREATE TABLE hasAuthor_Genre(
	author_genre_id varchar (255)  primary key,
	foreign key (author_genre_id) references Author_Genre(author_genre_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Edition(
	edition_id varchar (255)  primary key,
	edition_description varchar (255) not null,
	edition_label varchar (255) not null);

CREATE TABLE Author(
	author_label varchar (255) not null,
	author_description varchar (255) not null);

CREATE TABLE hasAnalog(
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasCityLocation(
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE locatedIn(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE foundedBy(
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE BookWrittenIn(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Character(
	character_id varchar (255)  primary key,
	character_label varchar (255) not null,
	character_description varchar (255) not null);

CREATE TABLE FictionalCharacter);

CREATE TABLE hasIllustrator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE FictionalHuman);

CREATE TABLE hasCountry(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasAfterwordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Translator(
	translator_label varchar (255) not null,
	translator_description varchar (255) not null);

CREATE TABLE hasMayor(
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE PlaceOfBirth(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE hasForewordAuthor(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasEdition(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasRole(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id));

CREATE TABLE FictionalNonHuman);

CREATE TABLE FictionalCity);

CREATE TABLE Language(
	num_speakers varchar (255),
	language_id varchar (255)  primary key,
	language_description varchar (255) not null,
	language_label varchar (255) not null);

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE City(
	city_label varchar (255) not null,
	city_description varchar (255) not null,
	city_id varchar (255)  primary key);

CREATE TABLE hasUsedLanguage(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE hasAward(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id),
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id));

CREATE TABLE PlaceOfDeath(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE Book(
	title varchar (255) not null,
	book_label varchar (255) not null,
	book_description varchar (255) not null,
	subtitle varchar (255),
	book_id varchar (255)  primary key);

CREATE TABLE hasCharacter(
	character_id varchar (255)  primary key,
	foreign key (character_id) references Character(character_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

