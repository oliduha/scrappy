try:
    import requests
    import bs4
    import os
    import json
    import csv
    import re

except ImportError as e:
    print("Erreur d'import : " + str(e))
    import requests
    import bs4
    import os
    import json
    import csv
    import re

# cf : https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
col_red = '\033[91m'
col_green = '\33[92m'
col_yellow = '\033[93m'
col_end = '\033[0m'


def scrap(links, make_csv=True, make_json=False, aio=False):
    list_titre = []
    list_a = []
    list_csv = []
    dict_json = {}
    file_name = ""

    for i in range(len(links)):
        file_name = links[i][0]
        link = links[i][1]
        # On récupère le contenu de la page en cours
        req_scrap = requests.get(link)

        print()
        print(col_yellow + "Lecture de la page : " + col_end)
        print(f"{file_name} [{links[i]}]")

        # On parse le html avec BeautifulSoup
        table = bs4.BeautifulSoup(req_scrap.content, "html.parser").find("table")

        list_b = table.findAll('b')  # On récupère tous les <b> de la table
        list_tr = table.findAll('tr')  # On récupère tous les <tr> de la table

        # On ajoute le texte des <b> dans la liste
        for t in list_b:
            list_titre.append(t.text)

        # Pour chaque ligne
        for tr in list_tr:
            list_td = tr.findAll('td')
            for td in list_td:
                list_p = td.find('p')
                for p in list_p:
                    # Si le contenu n'est pas un \n
                    if p != "\n":
                        # Si <a> est présent
                        if td.find('a'):
                            list_a.append(p.text.strip())
                        else:
                            list_a.append(p.text.strip())

        if make_csv:
            print(col_yellow + "Préparation des donnée csv..." + col_end)
            if i == 0:
                list_csv = [list_titre]
            if aio:
                list_csv += prepare_scv(list_a, file_name)
                file_name = "Port de 0 à 65535"
            else:
                list_csv = [list_titre]
                list_csv += prepare_scv(list_a, file_name)

        if make_json:
            print(col_yellow + "Préparation des donnée json..." + col_end)
            if aio:
                dict_json = {**dict_json, **prepare_json(list_tr, file_name)}
                file_name = "Port de 0 à 65535"
            else:
                dict_json = prepare_json(list_tr, file_name)

    if make_csv:
        create_scv(list_csv, file_name)
    if make_json:
        create_json(dict_json, file_name)


def prepare_scv(lst_a, csv_file_name):
    # CSV FILE ###################################################
    print(f"{col_yellow}Traitement des données de {csv_file_name} pour csv...{col_end}")

    # On supprime les 4 premiers éléments (les titres) de la liste
    list_elem = lst_a[4:]
    list_csv = []

    for i in range(0, len(list_elem), 4):
        list_csv.append(list_elem[i:i + 4])

    # On vérifie l'existence de l'arborescence et on la crée si besoin
    if not os.path.exists("exports/csv"):
        os.makedirs("exports/csv")

    return list_csv


def create_scv(data, csv_file_name):
    csv_file_name = csv_file_name.replace(" ", "_")
    # On écrit dans le fichier csv les éléments de chaque ligne
    with open("exports/csv/" + csv_file_name + '.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in data:
            writer.writerow(row)

    print(col_green + "Fichier " + csv_file_name + ".csv créé !" + col_end)


def prepare_json(list_tr, json_file_name):
    # JSON FILE #####################################################################
    print(f"{col_yellow}Traitement des données de {json_file_name} pour json...{col_end}")

    # Suppression des titres
    lines_soups = list_tr[1:]

    # 3. Structurer les données
    dict_json = {}
    for line_soup in lines_soups:
        columns_soups = line_soup.find_all("p")
        port_name = columns_soups[0].string.strip()
        port_number = int(columns_soups[1].find("a").string)  # Ajout du parsing
        port_protocol = columns_soups[2].find("a").string
        port_description = columns_soups[3].string.strip()

        if port_number not in dict_json:
            dict_json[port_number] = {}
        if port_protocol not in dict_json[port_number]:
            dict_json[port_number][port_protocol] = {}
        dict_json[port_number][port_protocol][port_name] = port_description

    return dict_json


def create_json(dict_json, json_file_name):
    json_file_name = json_file_name.replace(" ", "_")
    # On vérifie l'existence de l'arborescence
    if not os.path.exists("exports/json"):
        # Et on la crée si besoin
        os.makedirs("exports/json")

    # On écrit dans le fichier json les éléments de dict_json
    with open("exports/json/" + json_file_name + '.json', 'w', encoding='utf8') as jsonfile:
        json.dump(dict_json, jsonfile, indent=4)

    print(col_green + "Fichier " + json_file_name + ".json créé !" + col_end)


def test_cnx(url_cnx):
    # On récupère le contenu de la page en cours avec gestion des erreurs
    try:
        req_test = requests.get(url_cnx)
    except requests.ConnectionError as er:
        print(col_red + "\nErreur : Vérifiez votre connexion à Internet." + col_end)
        print(str(er))
        return False
    except requests.Timeout as er:
        print(col_red + "Erreur : Timeout." + col_end)
        print(str(er))
        return False
    except requests.RequestException as er:
        print(col_red + "Erreur générale." + col_end)
        print(str(er))
        return False
    except KeyboardInterrupt:
        print(col_yellow + "Le programme a été fermé", col_end)
        return False

    if req_test.status_code == 200:  # Si le site est en ligne
        print(col_green + 'OK, la page est en ligne !', col_end)
        return True
    else:
        # Si le site est en maintenance ou hors ligne
        print(col_red + "Erreur : La page renvoi le code d'état", req_test.status_code, col_end)
        return False


def read_headers(url_h):
    req_h = requests.get(url_h)
    print()
    print(col_yellow + "Headers :" + col_end)
    for header in req_h.headers:  # On affiche les headers
        print(header, req_h.headers[header])
    return req_h.headers


def cookies(url_c):
    print()
    print(f"{col_yellow}Cookies : {col_end}")
    # On récupère la session
    with requests.session() as session:
        req_c = session.get(url_c)
    for cok in req_c.cookies:
        print(cok)
    return req_c.cookies


def all_links(url_l):
    try:
        req_l = requests.get(url_l)
    except requests.ConnectionError as e:
        print(f"{col_red}\nErreur ! Vérifiez l'URL saisie :{col_end}")
        print(str(e))
        return {"ERREUR": "Vérifiez l'URL saisie"}
    except requests.Timeout as e:
        print(f"{col_red}\nErreur ! Timeout :{col_end}")
        print(str(e))
        return {"ERREUR": "Timeout"}
    except requests.RequestException as e:
        print(f"{col_red}\nErreur générale :{col_end}")
        print(str(e))
        return {"ERREUR": "Générale"}
    except KeyboardInterrupt:
        print(f"{col_yellow}\nLe programme a été fermé{col_end}")
        return {"ERREUR": "Le programme a été fermé"}
    except Exception as e:
        print("Erreur inconnue !" + str(e))
        return {"ERREUR": "inconnue"}

    print()
    print(f"{col_yellow}Liens : {col_end}")
    dict_links = {}

    # On parse le html avec BeautifulSoup
    page = bs4.BeautifulSoup(req_l.content, "html.parser").find("body")
    list_links = page.findAll('a')  # On récupère toutes les balises <a> de la page
    for link in list_links:
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9() \
                  @:%_\\+.~#?&\\/=]*)$"
        if link.string is None:
            link.string = "N.A."
        # On vérifie si URL est correcte
        if re.match(url_pattern, link["href"]):
            dict_links[link.string] = link["href"]
    nbl = 0
    for key in dict_links:
        nbl += 1
        print(f"{nbl}-[{key}] {dict_links[key]}")
    return dict_links


# Oli ############
# print(__name__)
if __name__ == "__main__":
    # url = "https://www.frameip.com/liste-des-ports.php/?plage=1"
    url = "https://www.google.com"
    # scrap(url)
    # read_headers(url)
    cookies(url)
##################

# Bryan ##########
# print(__name__)
# if __name__ == "__main__":
#     url = "https://www.frameip.com/liste-des-ports.php"
#     scrap(url)
#     read_headers(url)
#     cookies(url)
##################
