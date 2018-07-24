CREATE DATABASE bookDB;

USE bookDB;

CREATE TABLE locatedIn(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE hasAward(
	award_id varchar (255)  primary key,
	foreign key (award_id) references Award(award_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasIllustrator(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE RealCity(
	area varchar (255),
	population varchar (255));

CREATE TABLE hasCountryLocation(
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE Country(
	country_id varchar (255)  primary key,
	country_description varchar (255) not null,
	country_label varchar (255) not null);

CREATE TABLE Author(
	author_label varchar (255) not null,
	author_description varchar (255) not null);

CREATE TABLE Character(
	character_id varchar (255)  primary key,
	character_description varchar (255) not null,
	character_label varchar (255) not null);

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
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id),
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id));

CREATE TABLE Author_Genre(
	author_genre_id varchar (255)  primary key);

CREATE TABLE Edition(
	edition_description varchar (255) not null,
	edition_id varchar (255)  primary key,
	edition_label varchar (255) not null);

CREATE TABLE hasUsedLanguage(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	country_id varchar (255)  primary key,
	foreign key (country_id) references Country(country_id));

CREATE TABLE hasTranslator(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE PlaceOfDeath(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE followedBy(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id));

CREATE TABLE FictionalHuman);

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

CREATE TABLE InfluencedBy(
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE hasAnalog(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	fictionalcity_id varchar (255)  primary key,
	foreign key (fictionalcity_id) references FictionalCity(fictionalcity_id));

CREATE TABLE Award(
	award_id varchar (255)  primary key);

CREATE TABLE hasCityLocation(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	city_id varchar (255)  primary key,
	foreign key (city_id) references City(city_id));

CREATE TABLE Publisher(
	publisher_label varchar (255) not null,
	inception varchar (255) not null,
	publisher_description varchar (255) not null,
	publisher_id varchar (255)  primary key);

CREATE TABLE City(
	city_label varchar (255) not null,
	city_description varchar (255) not null,
	city_id varchar (255)  primary key);

CREATE TABLE Language(
	language_id varchar (255)  primary key,
	language_label varchar (255) not null,
	language_description varchar (255) not null,
	num_speakers varchar (255));

CREATE TABLE FictionalCharacter);

CREATE TABLE hasRole(
	mayor_id varchar (255)  primary key,
	foreign key (mayor_id) references Mayor(mayor_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE Book(
	book_description varchar (255) not null,
	book_label varchar (255) not null,
	book_id varchar (255)  primary key,
	title varchar (255) not null,
	subtitle varchar (255));

CREATE TABLE Mayor(
	end_time varchar (255),
	mayor_description varchar (255) not null,
	official_residence varchar (255) not null,
	mayor_id varchar (255)  primary key,
	start_time varchar (255) not null,
	mayor_label varchar (255) not null);

CREATE TABLE FictionalCity);

CREATE TABLE hasAuthor(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	author_id varchar (255)  primary key,
	foreign key (author_id) references Author(author_id));

CREATE TABLE Translator(
	translator_label varchar (255) not null,
	translator_description varchar (255) not null);

CREATE TABLE FictionalNonHuman);

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

CREATE TABLE PlaceOfBirth(
	realcity_id varchar (255)  primary key,
	foreign key (realcity_id) references RealCity(realcity_id),
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id));

CREATE TABLE foundedBy(
	human_id varchar (255)  primary key,
	foreign key (human_id) references Human(human_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE speaks(
	language_id varchar (255)  primary key,
	foreign key (language_id) references Language(language_id),
	translator_id varchar (255)  primary key,
	foreign key (translator_id) references Translator(translator_id));

CREATE TABLE hasPublisher(
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id),
	publisher_id varchar (255)  primary key,
	foreign key (publisher_id) references Publisher(publisher_id));

CREATE TABLE hasEdition(
	book_id varchar (255)  primary key,
	foreign key (book_id) references Book(book_id),
	edition_id varchar (255)  primary key,
	foreign key (edition_id) references Edition(edition_id));

CREATE TABLE Human(
	sex varchar (255) not null,
	DoD varchar (255),
	human_label varchar (255) not null,
	name varchar (255) not null,
	DoB varchar (255) not null,
	human_id varchar (255)  primary key,
	human_description varchar (255) not null);

