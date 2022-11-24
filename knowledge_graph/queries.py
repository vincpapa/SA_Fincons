import requests
import time


def unique(lista):
    return list(set(lista))


def uri(label_film):
    '''
    function to execute a query on dbpedia
    '''
    # print(str(int(label_film[-4:]) + 1), str(int(label_film[-4:]) - 1))
    url = 'https://dbpedia.org/sparql'
    query = """SELECT * 
               WHERE {?s rdf:type dbo:Film .
               ?s rdfs:label ?label .           
               ?label bif:contains '""" + '"' + label_film + '"' + """' OPTION (score ?sc) .
               FILTER (?sc > 10) .
               FILTER langMatches(lang(?label),'en')
               } 
               ORDER BY DESC (?sc)
               LIMIT 1
            """
    r = requests.get(url, params={'format': 'json', 'query': query})
    if r.status_code == 200:
        if not r.json()['results']['bindings']:
            uri = ''
        else:
            uri = r.json()['results']['bindings'][0]['s']['value']
    # elif r.status_code == 429:
    #    # print('-- STATUS CODE -- ' + str(r.status_code) + '--' + str(element_id))
    #    time.sleep(2)
    #    r = requests.get(url, params={'format': 'json', 'query': query})
    # elif r.status_code == 500:
    #    # print('-- STATUS CODE -- ' + str(r.status_code) + '--' + str(element_id))
    #    time.sleep(2)
    #    sub_entity_ids = query_subclass(element_id)
    #    for sub_entity_id in sub_entity_ids:
    #        splitted_entities = splitting_entities(sub_entity_id, splitted_entities)
    else:
        print(f'--- STATUS CODE DIFFERENT --- {r.status_code} for entity {label_film}')
    time.sleep(0.2)
    return uri


def infos(uri):
    url = 'https://dbpedia.org/sparql'
    query = """select ?l_director ?l_starring ?l_distributor ?l_editing ?l_musicComposer ?l_producer 
    where""" + """{""" + """<{uri}> dbo:director ?director .
    <{uri}> dbo:starring ?starring. 
    <{uri}> dbo:distributor ?distributor .
    <{uri}> dbo:editing ?editing .
    <{uri}> dbo:musicComposer ?musicComposer .
    <{uri}> dbo:producer ?producer .
    ?director rdfs:label ?l_director .  
    ?starring rdfs:label ?l_starring .  
    ?distributor rdfs:label ?l_distributor .  
    ?editing rdfs:label ?l_editing .  
    ?musicComposer rdfs:label ?l_musicComposer .  
    ?producer rdfs:label ?l_producer .  
    FILTER langMatches(lang(?l_director),'en') .
    FILTER langMatches(lang(?l_starring),'en') .
    FILTER langMatches(lang(?l_distributor),'en') .
    FILTER langMatches(lang(?l_editing),'en') .
    FILTER langMatches(lang(?l_musicComposer),'en') .
    FILTER langMatches(lang(?l_producer),'en') .""".format(uri=uri) + """}"""
    directors = []
    starring = []
    distributor = []
    editing = []
    musiccomposer = []
    producer = []
    r = requests.get(url, params={'format': 'json', 'query': query})
    if r.status_code == 200:
        if not r.json()['results']['bindings']:
            pass
        else:
            for i in range(len(r.json()['results']['bindings'])):
                directors.append(r.json()['results']['bindings'][i]['l_director']['value'])
                starring.append(r.json()['results']['bindings'][i]['l_starring']['value'])
                distributor.append(r.json()['results']['bindings'][i]['l_distributor']['value'])
                editing.append(r.json()['results']['bindings'][i]['l_editing']['value'])
                musiccomposer.append(r.json()['results']['bindings'][i]['l_musicComposer']['value'])
                producer.append(r.json()['results']['bindings'][i]['l_producer']['value'])
        directors = list(set(directors))
        starring = list(set(starring))
        distributor = list(set(distributor))
        editing = list(set(editing))
        musiccomposer = list(set(musiccomposer))
        producer = list(set(producer))
    else:
        print(f'--- STATUS CODE DIFFERENT --- {r.status_code} for entity {uri}')
    time.sleep(0.2)
    return directors, starring, distributor, editing, musiccomposer, producer

