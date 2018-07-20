
# coding: utf-8

# In[1]:


#parser: given owl, set up db and write mappings


# In[2]:


with open ("../books/books18_07.owl", "r") as fowl:
    content = fowl.read()
    i = 0
    lines = content.split("\n")
    outstring = ""
    dict_classes = {}
    dict_relations = {}
    dict_attributes = {}
    while (i < len(lines)):
        
        line = lines[i]
        
        if ("follows") in line or ("bo:author_genre" in line and "bo:Book" in line):
            i += 1
            continue
        
        if "Prefix" in lines[i]:
            i += 1
            continue

        if "Declaration(Class" in lines[i]: #from now on, work on this class
            classe = line.split(":")[1][:-2]
            dict_classes[classe] = {}
            dict_classes[classe]["attributes"] = {}
            i += 1
            continue
            
        if "Declaration(ObjectProperty" in lines[i]:
            relation = line.split(":")[1][:-2]
            dict_relations[relation] = {}
            dict_relations[relation]["functional"] = False
            dict_relations[relation]["inv_functional"] = False
            i += 1
            continue
        
        if "Declaration(DataProperty" in lines[i]:
            attribute = line.split(":")[1][:-2]
            dict_attributes[attribute] = {}
            dict_attributes[attribute]["functional"] = False
            dict_attributes[attribute]["inv_functional"] = False
            i += 1
            continue
            
        if "ObjectPropertyDomain" in lines[i]:
            relation = line.split(" ")[0].split(":")[-1]
            domain = line.split(":")[-1][:-1]
            dict_relations[relation]["domain"] = {}
            dict_relations[relation]["domain"]["name"] = domain
            dict_relations[relation]["domain"]["nullable"] = True
            i += 1
            continue
            
        if "DataPropertyDomain" in lines[i]:
            attribute = line.split(" ")[0].split(":")[-1]
            domain = line.split(":")[-1][:-1]
            dict_attributes[attribute]["domain"] = {}
            dict_attributes[attribute]["domain"]["name"] = domain
            dict_attributes[attribute]["domain"]["nullable"] = True
            i += 1
            continue
        
        if "ObjectPropertyRange" in lines[i]:
            relation = line.split(" ")[0].split(":")[-1]
            range_ = line.split(":")[-1][:-1]
            dict_relations[relation]["range"] = {}
            dict_relations[relation]["range"]["name"] = range_
            dict_relations[relation]["range"]["nullable"] = True
            i += 1
            continue
            
        if "DataPropertyRange" in lines[i]:
            attribute = line.split(" ")[0].split(":")[-1]
            range_ = line.split(":")[-1][:-1]
            dict_attributes[attribute]["range"] = {}
            dict_attributes[attribute]["range"]["name"] = range_
            #dict_attributes[attribute]["range"]["nullable"] = True
            i += 1
            continue
        
        if "FunctionalObjectProperty" in lines[i]:
            relation = line.split(":")[-1][:-1]
            dict_relations[relation]["functional"] = True
            i += 1
            continue
            
        if "FunctionalDataProperty" in lines[i]:
            attribute = line.split(":")[-1][:-1]
            dict_attributes[attribute]["functional"] = True
            i += 1
            continue

        if "EquivalentClasses" in lines[i] and "Thing" in lines[i]:
            relation = line.split(":")[2].split(" ")[0].replace(")", "")
            if "ObjectInverseOf" not in lines[i]:
                domain = line.split(":")[1].split(" ")[0]
                dict_relations[relation]["domain"]["nullable"] = False
            else:
                range_ = line.split(":")[1].split(" ")[0]
                dict_relations[relation]["range"]["nullable"] = False
            i += 1
            continue
            
        if "EquivalentClasses" in lines[i] and "rdf" in lines[i]:
            attribute = line.split(":")[2].split(" ")[0].replace(")", "")
            domain = line.split(":")[1].split(" ")[0]
            dict_attributes[attribute]["domain"]["nullable"] = False #no need to work on the range
            i += 1
            continue
            
        i += 1

print(dict_classes)
print("************************")
print (dict_relations)
print("************************")
print (dict_attributes)
    
    
    
    


# In[3]:


relazioni_da_accorpare = ["hasMayor"]
relazioni_da_accorpare = []
#'character_id': {'range': {'name': 'character_id> xsd:strin'}, 'domain': {'name': 'Character', 'nullable': False}, 'functional': True, 'inv_functional': False}


# In[4]:


#dict_attributes.keys()


# In[5]:


for attribute in dict_attributes.keys():
    if dict_attributes[attribute]["functional"] == False: #va reificata la ER-relazione e creata una nuova relazione
        #print(attribute, "**********attr")
        new_class = attribute.title()
        dict_classes[new_class] = {}
        dict_classes[new_class]["attributes"] = {}
        attribute_name = new_class.lower() + "_id"
        dict_classes[new_class]["attributes"][attribute_name] = {}
        dict_classes[new_class]["attributes"][attribute_name]["typ"] = "varchar (255)"
        dict_classes[new_class]["attributes"][attribute_name]["nullable"] = False

        new_relation = "has" + attribute.title()
        dict_relations[new_relation] = {}
        dict_relations[new_relation]["domain"] = {}
        dict_relations[new_relation]["domain"]["name"] = dict_attributes[attribute]["domain"]["name"]
        dict_relations[new_relation]["domain"]["nullable"] = dict_attributes[attribute]["domain"]["nullable"]
        dict_relations[new_relation]["range"] = {}
        dict_relations[new_relation]["range"]["name"] = new_class
        dict_relations[new_relation]["range"]["nullable"] = False
        dict_relations[new_relation]["functional"] = False
        dict_relations[new_relation]["inv_functional"] = False
    else: #assign attributes to classes
        class_ = dict_attributes[attribute]["domain"]["name"]
        #print(class_)
        nullable = dict_attributes[attribute]["domain"]["nullable"]
        typ = "varchar (255)"
        dict_classes[class_]["attributes"][attribute] = {}
        dict_classes[class_]["attributes"][attribute]["typ"] = typ
        dict_classes[class_]["attributes"][attribute]["nullable"] = nullable


for relation in dict_relations.keys():
    if relation in relazioni_da_accorpare and dict_relations[relation]["functional"] == True: #va accorpata, con precedenza sul dominio
        #print(relation, "**********")
        class_ = dict_relations[relation]["domain"]["name"]
        new_attribute = dict_relations[relation]["range"]["name"]
        nullable = dict_relations[relation]["domain"]["nullable"]
        typ = "varchar (255)"
        dict_classes[class_]["attributes"][relation] = {}
        dict_classes[class_]["attributes"][relation]["typ"] = typ
        dict_classes[class_]["attributes"][relation]["nullable"] = nullable
    elif relation in relazioni_da_accorpare and dict_relations[relation]["inv_functional"] == True:
        #print(relation, "*INV**********")
        class_ = dict_relations[relation]["range"]["name"]
        new_attribute = dict_relations[relation]["domain"]["name"]
        nullable = dict_relations[relation]["range"]["nullable"]
        typ = "varchar (255)"
        dict_classes[class_]["attributes"][relation] = {}
        dict_classes[class_]["attributes"][relation]["typ"] = typ
        dict_classes[class_]["attributes"][relation]["nullable"] = nullable
        dict_classes[class_]["attributes"][relation]["references"] = new_attribute
    else: 
        print(relation)
        domain = dict_relations[relation]["domain"]["name"]
        range_ = dict_relations[relation]["range"]["name"]
        dict_classes[relation] = {}
        dict_classes[relation]["attributes"] = {}
        dict_classes[relation]["attributes"][domain.lower() + "_id"] = {}
        dict_classes[relation]["attributes"][domain.lower() + "_id"]["references"] = domain
        dict_classes[relation]["attributes"][domain.lower() + "_id"]["typ"] = "varchar (255)"
        dict_classes[relation]["attributes"][domain.lower() + "_id"]["nullable"] = dict_relations[relation]["domain"]["nullable"]
        dict_classes[relation]["attributes"][range_.lower() + "_id"] = {}
        dict_classes[relation]["attributes"][range_.lower() + "_id"]["references"] = range_
        dict_classes[relation]["attributes"][range_.lower() + "_id"]["typ"] = "varchar (255)"
        dict_classes[relation]["attributes"][range_.lower() + "_id"]["nullable"] = dict_relations[relation]["range"]["nullable"]


print(dict_classes)
print("************************")
'''print (dict_relations)
print("************************")
print (dict_attributes)    
print("************************")       '''


    
    


# In[6]:


#generate strings and write to file


# In[12]:


outstring_create = "CREATE DATABASE bookDB;\n\nUSE bookDB;\n\n"
outstring_insert = ""

with open("create.sql", "w") as cf, open("insert.sql", "w") as insf:
    for class_ in dict_classes.keys():
        referencing = False
        outstring_create += "CREATE TABLE " + class_ + "(" + "\n"
        #print(class_)
        for attribute in dict_classes[class_]["attributes"]:
            outstring_create += "\t" + attribute
            outstring_create +=   " " + dict_classes[class_]["attributes"][attribute]["typ"] 
            if "_id" in attribute:
                outstring_create += " " + " primary key"
            elif not dict_classes[class_]["attributes"][attribute]["nullable"]:
                outstring_create += " " + "not null"
            outstring_create += ",\n"
            if "references" in (dict_classes[class_]["attributes"][attribute]).keys():
                referencing = True
                outstring_create += "\tforeign key " +                 "("+ attribute + ") references " +                 dict_classes[class_]["attributes"][attribute]["references"] + "(" +                 dict_classes[class_]["attributes"][attribute]["references"].lower() + "_id),\n"
        '''for attribute in dict_classes[class_]["attributes"]:
            if "references" in (dict_classes[class_]["attributes"][attribute]).keys():
                outstring_create += "\tprimary key (" + attribute + "," + \
                dict_classes[class_]["attributes"][attribute]["references"].lower() + "_id),\n"'''
        outstring_create = outstring_create.rstrip()[:-1] #remove comma and newline
        outstring_create += ");\n\n" 

        if referencing:
            relative_path = "../roles/" + class_
        else:
            relative_path = "../concepts/" + class_
        outstring_insert += "LOAD DATA LOCAL INFILE " +  relative_path + ".txt INTO TABLE " + class_ + "\nFIELDS TERMINATED BY ';'\nENCLOSED BY '\"'"+        "\nLINES TERMINATED BY '\\n'\nIGNORE 1 LINES;\n\n"


    print(outstring_create)
    print(outstring_insert)
    insf.write(outstring_insert)
    cf.write(outstring_create)


# In[42]:


base_iri = "http://books/"
outstring_mappings = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + "<OBDA version=\"1.0\">\n" +     "<dataSource databaseDriver=\"org.postgresql.Driver\" databaseName=\"\"\n"+        "databasePassword=\"postgres\"\n"+        "databaseURL=\"jdbc:postgresql://localhost/comics_db\"\n"+        "databaseUsername=\"postgres\" name=\"datasource\"/>\n"+    "<prefixes>\n"+        "<prefix name=\"owl:\" namespace=\"http://www.w3.org/2002/07/owl#\"/>\n"+        "<prefix name=\"rdf:\" namespace=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"/>\n"+        "<prefix name=\"sh:\" namespace=\"" + base_iri + "/#>\n"+        "<prefix name=\"xsd:\" namespace=\"http://www.w3.org/2001/XMLSchema#\"/>\n"+        "<prefix name=\":\" namespace=\"" + base_iri + ">\n"+        "<prefix name=\"xml:\" namespace=\"http://www.w3.org/XML/1998/namespace\"/>\n"+        "<prefix name=\"rdfs:\" namespace=\"http://www.w3.org/2000/01/rdf-schema#\"/>\n"+    "</prefixes>\n"

with open("book_mappings.xml", "w") as mapf:
    
    #templates
    outstring_mappings += "<templates>\n"
    for class_ in dict_classes.keys():
        outstring_mappings += "<template>http://books/" + class_.lower() + "_{_}</template>\n"
    outstring_mappings += "</templates>\n"
    
    #mappings, sql included
    outstring_mappings += "<mappings>\n"
    mapping_counter = 0
    for class_ in dict_classes.keys():
        mapping_counter += 1
        attributes_set = set()
        from_relation = False
        for attribute in dict_classes[class_]["attributes"]:
            attributes_set.add(attribute)
            if "references" in (dict_classes[class_]["attributes"][attribute]).keys():
                from_relation = True
        if from_relation:
            word = "role"
            domain = "DOM"
            range_ = "RANGE"
        else:
            word = "concept"
        query = "SELECT "
        head_string = "\n<HEAD string=\"" + class_ + "_view("
        for attr in attributes_set:
            query += class_[0].lower() + "." + attr + " AS " + attr + ", "
            head_string += attr + ", "
        head_string = head_string[:-2]
        head_string += ")\"/>"
        query = query[:-2]
        query += " FROM book_db." + class_ + " " + class_[0].lower()
        outstring_mappings += "\n<ontologyPredicateMapping id=\"M" + str(mapping_counter) + "_" + class_ + "\">" +         "\n<" + word + " string=" + base_iri + "#" + class_ + ">"
        if not from_relation:
            outstring_mappings += "\n<template>" + base_iri + class_.lower() + "{" + class_.lower() + "_id}" + "</template>"
        else:
            outstring_mappings += "\n<domainTemplate>" + base_iri + domain + "{" + domain + "_id}" + "</domainTemplate>\n<rangeTemplate>" + base_iri + base_iri + range_ + "{" + range_ + "_id}" + "</rangeTemplate>"
        outstring_mappings += "\n</" + word + ">"
        outstring_mappings += head_string + "\n</ontologyPredicateMapping>\n"
        
        for attr in attributes_set:
            mapping_counter += 1
            outstring_mappings += "\n<ontologyPredicateMapping id=\"M" + str(mapping_counter) + "_" + attr + "\">" +             "\n<" + "attribute" + " string=" + base_iri + "#" + class_ + ">"
            outstring_mappings += "\n<domainTemplate>" + base_iri + class_.lower() + "{" + class_.lower() + "_id}" + "</domainTemplate>"
            outstring_mappings += "\n<rangeVariable>" + attr + "</rangeVariable> "+ "\n</" + word + ">"
            outstring_mappings += head_string + "\n</ontologyPredicateMapping>\n"
        
        outstring_mappings += "\n<primitiveView>" + "\n<HEAD string=\"" + class_ + "_view(" + class_ + "_id)\"/>" 
        outstring_mappings += "\n<SQLQuery> " + query + " </SQLQuery>\n</primitiveView>\n"
    outstring_mappings += "</mappings>\n<blocks/>\n<constraints/>\n</OBDA>"

    print (outstring_mappings)

