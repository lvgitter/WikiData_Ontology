CREATE DATABASE bookDB;

USE bookDB;

/* CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci */

CREATE TABLE Book (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255),
    Title varchar(255),
    Subtitle varchar(255),
    FirstLine varchar(255),
    Series varchar(255)
);

/*Author ISA?*/
CREATE TABLE Author (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255),
    Name varchar(255),
    Sex varchar(255),
    FirstLine varchar(255),
    Series varchar(255)
);

CREATE TABLE Genre (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255)
);

CREATE TABLE Publisher (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255),
    Inception varchar(255)
);


CREATE TABLE Edition (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255),
    Title varchar(255),
    Subtitle varchar(255),
    FirstLine varchar(255),
    Illustrator varchar(255), /* does a book have more than 1 ill? more than 1 transl? */
    Translator varchar(255)
);

/*
CREATE TABLE Publisher (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255),
    Founder varchar(255),
    foreign key(Founder) references Human(Id)
);
*/

CREATE TABLE Illustrator (
    Id varchar(255) primary key /* inherits from humans --NO ISA here*/
);

CREATE TABLE Characters (
    Id varchar(255) primary key,
    Label varchar(255),
    Description varchar(255),
    Name varchar(255),
    DoB varchar(255),
    DoD varchar(255),
    Sex varchar(255)
);


CREATE TABLE Language (
    Id varchar(255) primary key,
    Label varchar(255),
    Speakers int
);







CREATE TABLE hasGenre (
    BookId varchar(255),
    GenreId varchar(255),
    foreign key (BookId) references Book(Id),
    foreign key (GenreId) references Genre(Id),
    primary key (BookId,GenreId)
);

CREATE TABLE hasPublisherBOOK (
    BookId varchar(255),
    PublisherId varchar(255),
    foreign key (BookId) references Book(Id),
    foreign key (PublisherId) references Publisher(Id),
    primary key (BookId,PublisherId)
);


CREATE TABLE hasPublisherEDITION (
    EditionId varchar(255),
    PublisherId varchar(255),
    foreign key (EditionId) references Edition(Id),
    foreign key (PublisherId) references Publisher(Id),
    primary key (EditionId,PublisherId)
);

CREATE TABLE hasCharacter (
    BookId varchar(255),
    CharacterId varchar(255),
    foreign key (BookId) references Book(Id),
    foreign key (CharacterId) references Characters(Id),
    primary key (BookId,CharacterId)
);

CREATE TABLE hasLanguage (
    BookId varchar(255),
    LanguageId varchar(255),
    foreign key (BookId) references Book(Id),
    foreign key (LanguageId) references Language(Id),
    primary key (BookId,LanguageId)
);




--        "no title": 0,
--        "no label": 1,
--        "no description": 2,
--        "no author": 3,
--        "multiple author": 4,
--        "no genre": 5,
--        "no subtitle": 6,
--        "no first line": 7,
--        "no pub": 8,
--        "no char": 9,
--        "no loc": 10,
--        "no afterauthor": 11,
--        "no foreauthor": 12,
--        "no lang": 13,
--        "no ill": 14,
--        "no editions": 15,
--        "no series": 16,
--        "no follower": 17,
--        "no character":18

