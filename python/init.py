import subprocess
import os
import datetime

# DICTIONARIES (delete old ones)

dicts = [
    "awards.pkl",
    "genres.pkl",
    "locations.pkl",
    "occupations.pkl",
    "official_residence.pkl",
    "series.pkl"
        ]

for dict in dicts:
    os.remove("obj/"+dict)

# PROCESSED CONCEPTS
processed_concepts = [
    "processedAuthors.txt",
    "processedHumans.txt",
    "processedBooks.txt",
    "processedLanguages.txt",
    "processedCharacters.txt",
    "processedMayors.txt",
    "processedCities.txt",
    "processedPublishers.txt",
    "processedCountries.txt",
    "processedTranslators.txt",
    "processedEditions.txt"]

for processed_concept in processed_concepts:
    try:
        os.remove("../processed/" + processed_concept)
    except OSError:
        pass
    file = open("../processed/" + processed_concept, 'w')
    file.write("id\n")
    file.close()

# CONCEPTS
books_file_path = "../concepts/Book.txt"
books_file = open(books_file_path, 'w')
books_file.write("book_id;book_label;book_description;title;subtitle;first_line;series\n")
books_file.close()

authors_file_path = "../concepts/Author.txt"
authors_file = open(authors_file_path, 'w')
authors_file.write('human_id;human_label;human_description;human_name;human_sex;human_DoB;human_DoD\n')
authors_file.close()

fictional_humans_file_path = "../concepts/FictionalHuman.txt"
fictional_humans_file = open(fictional_humans_file_path, 'w')
fictional_humans_file.write('character_id;character_label;character_description;character_name;character_sex;character_DoB;character_DoD\n')
fictional_humans_file.close()

fictional_not_humans_file_path = "../concepts/FictionalNotHuman.txt"
fictional_not_humans_file = open(fictional_not_humans_file_path, 'w')
fictional_not_humans_file.write('character_id;character_label;character_description;character_name;character_sex;character_DoB;character_DoD\n')
fictional_not_humans_file.close()

real_cities_file_path = "../concepts/RealCity.txt"
real_cities_file = open(real_cities_file_path, 'w')
real_cities_file.write("city_id;city_label;city_description;realCity_area;realCity_population\n")
real_cities_file.close()

fictional_cities_file_path = "../concepts/FictionalCity.txt"
fictional_cities_file = open(fictional_cities_file_path, 'w')
fictional_cities_file.write("city_id;city_label;city_description\n")
fictional_cities_file.close()

countries_file_path = "../concepts/Country.txt"
countries_file = open(countries_file_path, 'w')
countries_file.write("country_id;country_label;country_description;country_area;country_population\n")
countries_file.close()

editions_file_path = "../concepts/Edition.txt"
editions_file = open(editions_file_path, 'w')
editions_file.write("edition_id;edition_label;edition_description\n")
editions_file.close()

humans_file_path = "../concepts/Human.txt"
humans_file = open(humans_file_path, 'w')
humans_file.write('human_id;human_label;human_description;human_name;human_sex;human_DoB;human_DoD;is_character\n')
humans_file.close()

languages_file_path = "../concepts/Language.txt"
languages_file = open(languages_file_path, 'w')
languages_file.write("language_id;language_label;language_description;speakers\n")
languages_file.close()

mayors_file_path = "../concepts/Mayor.txt"
mayors_file = open(mayors_file_path, 'w')
mayors_file.write('mayor_id;mayor_label;mayor_description;start_time;end_time;official_residence\n')
mayors_file.close()

publishers_file_path = "../concepts/Publisher.txt"
publishers_file = open(publishers_file_path, 'w')
publishers_file.write("publisher_id;publisher_label;publisher_description;inception\n")
publishers_file.close()

translators_file_path = "../concepts/Translator.txt"
translators_file = open(translators_file_path, 'w')
translators_file.write("human_id;human_label;human_description;human_name;human_sex;human_DoB;human_DoD\n")
translators_file.close()

# ROLES

has_afterword_file_path = "../roles/hasAfterwordAuthor.txt"
has_afterword_file = open(has_afterword_file_path, 'w')
has_afterword_file.write("book_id;afterauthor_id\n")
has_afterword_file.close()

has_foreword_file_path = "../roles/hasForewordAuthor.txt"
has_foreword_file = open(has_foreword_file_path, 'w')
has_foreword_file.write("book_id;foreauthor_id\n")
has_foreword_file.close()

influenced_by_file_path = "../roles/influencedBy.txt"
influenced_by_file = open(influenced_by_file_path, 'w')
influenced_by_file.write('author_id;influencing_author_id\n')
influenced_by_file.close()

place_of_birth_file_path = "../roles/placeOfBirth.txt"
place_of_birth_file = open(place_of_birth_file_path, 'w')
place_of_birth_file.write('human_id;realCity_id\n')
place_of_birth_file.close()

place_of_death_file_path = "../roles/placeOfDeath.txt"
place_of_death_file = open(place_of_death_file_path, 'w')
place_of_death_file.write('human_id;realCity_id\n')
place_of_death_file.close()

has_awards_file_path = "../roles/hasAuthorAwards.txt"
has_awards_file = open(has_awards_file_path, 'w')
has_awards_file.write("author_id;award\n")
has_awards_file.close()

author_has_genres_file_path = "../roles/hasAuthorGenres.txt"
author_has_genres_file = open(author_has_genres_file_path, 'w')
author_has_genres_file.write("author_id;genre\n")
author_has_genres_file.close()

has_author_file_path = "../roles/hasAuthor.txt"
has_author_file = open(has_author_file_path, 'w')
has_author_file.write("book_id;author_id\n")
has_author_file.close()

has_city_location_file_path = "../roles/hasCityLocation.txt"
has_city_location_file = open(has_city_location_file_path, 'w')
has_city_location_file.write("book_id;city_id\n")
has_city_location_file.close()

has_country_location_file_path = "../roles/hasCountryLocation.txt"
has_country_location_file = open(has_country_location_file_path, 'w')
has_country_location_file.write("book_id;country_id\n")
has_country_location_file.close()

has_character_file_path = "../roles/hasCharacter.txt"
has_character_file = open(has_character_file_path, 'w')
has_character_file.write("book_id;character_id\n")
has_character_file.close()

written_in_file_path = "../roles/writtenIn.txt"
written_in_file = open(written_in_file_path, 'w')
written_in_file.write("book_id;language_id\n")
written_in_file.close()

has_translator_file_path = "../roles/hasTranslator.txt"
has_translator_file = open(has_translator_file_path, 'w')
has_translator_file.write("edition_id;translator_id\n")
has_translator_file.close()

has_edition_file_path = "../roles/hasEdition.txt"
has_edition_file = open(has_edition_file_path, 'w')
has_edition_file.write("book_id;edition_id\n")
has_edition_file.close()

follows_file_path = "../roles/follows.txt"
follows_file = open(follows_file_path, 'w')
follows_file.write("book_id;followed_book_id\n")
follows_file.close()

book_has_genres_file_path = "../roles/hasBookGenres.txt"
book_has_genres_file = open(book_has_genres_file_path, 'w')
book_has_genres_file.write("book_id;genre\n")
book_has_genres_file.close()

has_country_file_path = "../roles/hasCountry.txt"
has_country_file = open(has_country_file_path, 'w')
has_country_file.write("city_id;country_id\n")
has_country_file.close()

has_mayor_file_path = "../roles/hasMayor.txt"
has_mayor_file = open(has_mayor_file_path, 'w')
has_mayor_file.write("city_id;mayor_id\n")
has_mayor_file.close()

has_analog_file_path = "../roles/hasAnalog.txt"
has_analog_file = open(has_analog_file_path, 'w')
has_analog_file.write("fictionalCity_id;realCity_id\n")
has_analog_file.close()

has_used_language_file_path = "../roles/hasUsedLanguage.txt"
has_used_language_file = open(has_used_language_file_path, 'w')
has_used_language_file.write("country_id;language_id\n")
has_used_language_file.close()

has_illustrator_file_path = "../roles/hasIllustrator.txt"
has_illustrator_file = open(has_illustrator_file_path, 'w')
has_illustrator_file.write("edition_id;illustrator_id\n")
has_illustrator_file.close()

has_publisher_file_path = "../roles/hasPublisher.txt"
has_publisher_file = open(has_publisher_file_path, 'w')
has_publisher_file.write("edition_id;publisher_id\n")
has_publisher_file.close()

human_has_occupations_file_path = "../roles/hasHumanOccupation.txt"
human_has_occupations_file = open(human_has_occupations_file_path, 'w')
human_has_occupations_file.write("human_id;occupation\n")
human_has_occupations_file.close()

has_role_file_path = "../roles/hasRole.txt"
has_role_file = open(has_role_file_path, 'w')
has_role_file.write('human_id;mayor_id\n')
has_role_file.close()

located_in_file_path = "../roles/locatedIn.txt"
located_in_file = open(located_in_file_path, 'w')
located_in_file.write("publisher_id;country_id;\n")
located_in_file.close()

founded_by_file_path = "../roles/foundedBy.txt"
founded_by_file = open(founded_by_file_path, 'w')
founded_by_file.write("publisher_id;human_id\n")
founded_by_file.close()

speaks_file_path = "../roles/speaks.txt"
speaks_file = open(speaks_file_path, 'w')
speaks_file.write("translator_id;language_id\n")
speaks_file.close()


# TMP

human_character_file_path = "../tmp/human_character.txt"
human_character_file = open (human_character_file_path, 'w')
human_character_file.write("human_id\n")
human_character_file.close()

# LOGS
timestamp = '{:%Y-%m-%d %H:%M:%S}\n\n'.format(datetime.datetime.now())

book_log_file_path = "../log/log_Book.txt"
book_log_file = open(book_log_file_path, 'w')
book_log_file.write(timestamp)
book_log_file.close()

author_log_file_path = "../log/log_Author.txt"
author_log_file = open(author_log_file_path, 'w')
author_log_file.write(timestamp)
author_log_file.close()

character_log_file_path = "../log/log_Characters.txt"
character_log_file = open(character_log_file_path, 'w')
character_log_file.write(timestamp)
character_log_file.close()

city_log_file_path = "../log/log_City.txt"
city_log_file = open(city_log_file_path, 'w')
city_log_file.write(timestamp)
city_log_file.close()

country_log_file_path = "../log/log_Country.txt"
country_log_file = open(country_log_file_path, 'w')
country_log_file.write(timestamp)
country_log_file.close()

edition_log_file_path = "../log/log_Edition.txt"
edition_log_file = open(edition_log_file_path, 'w')
edition_log_file.write(timestamp)
edition_log_file.close()

human_log_file_path = "../log/log_Human.txt"
human_log_file = open(human_log_file_path, 'w')
human_log_file.write(timestamp)
human_log_file.close()

human_character_log_file_path = "../log/log_HumanCharacters.txt"
human_character_log_file = open(human_character_log_file_path, 'w')
human_character_log_file.write(timestamp)
human_character_log_file.close()

language_log_file_path = "../log/log_Language.txt"
language_log_file = open(language_log_file_path, 'w')
language_log_file.write(timestamp)
language_log_file.close()

mayor_log_file_path = "../log/log_Mayor.txt"
mayor_log_file = open(mayor_log_file_path, 'w')
mayor_log_file.write(timestamp)
mayor_log_file.close()

publisher_log_file_path= "../log/log_Publisher.txt"
publisher_log_file = open(publisher_log_file_path, 'w')
publisher_log_file.write(timestamp)
publisher_log_file.close()

translator_log_file_path = "../log/log_Translator.txt"
translator_log_file = open(translator_log_file_path, 'w')
translator_log_file.write(timestamp)
translator_log_file.close()

programs = [
    "books_download.py",
    "authors_download.py",
    "characters_download.py",
    "publishers_download.py",
    "languages_download.py",
    "editions_download.py",
    "translator_download.py",
    "human_download.py",
    "character_human_download.py",
    "cities_download.py",
    "countries_download.py",
    "mayor_download.py"
]

for iteration in range(10):
    completed = []
    count = 0
    for program in programs:
        if int(subprocess.call("python " + program, shell=True))==1:
            completed.append(program)
            count += 1
    print(" * * * * * * * * * * * * * * * * * * * *\nIteration n. "+str(iteration)+"\n")
    print("missing programs = "+str(list(set(programs).difference(set(completed))))+"\n\n\n\n")
    if count==len(programs):
        break

