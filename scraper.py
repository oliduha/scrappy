try:
    import requests
    import bs4
    import os
    import json
    import csv

except ImportError as e:
    print("Erreur d'import : " + str(e))
    import requests
    import bs4
    import os
    import json
    import csv


# cf : https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
col_red = '\033[91m'
col_green = '\33[92m'
col_yellow = '\033[93m'
col_end = '\033[0m'
list_a = []
list_titre = []


def scrap(url_scrap='https://www.frameip.com/liste-des-ports-tcp-udp/?plage=1',
          file_name="file_name", make_csv=True, make_json=False):

    # On récupère le contenu de la page en cours
    req_scrap = requests.get(url_scrap)

    print()
    print(col_yellow + "Page à traiter : " + col_end)
    print(url_scrap)

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
        create_scv(file_name)

    if make_json:
        create_json(file_name, list_tr)


def create_scv(csv_file_name):
    # CSV FILE ###################################################
    print(f"{col_yellow}Création du fichier {csv_file_name}.csv...{col_end}")
    # On supprime les 4 premiers éléments (les titres) de la liste
    list_elem = list_a[4:]

    copy_el = list_elem
    list_csv = [list_titre]

    for i in range(0, len(list_elem), 4):
        list_csv.append(copy_el[i:i + 4])

    # On vérifie l'existence de l'arborescence et on la crée si besoin
    if not os.path.exists("exports/csv"):
        os.makedirs("exports/csv")
    # On écrit dans le fichier csv les éléments de chaque ligne
    with open("exports/csv/"+csv_file_name+'.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in list_csv:
            writer.writerow(row)

    print(col_green + "Fichier "+csv_file_name+".csv créé !" + col_end)


def create_json(json_file_name, list_tr):
    # JSON FILE #####################################################################
    # On crée un dictionnaire avec les listes de titres et d'éléments de chaque ligne
    list_data = []
    print(f"{col_yellow}Création du fichier {json_file_name}.json...{col_end}")
    for tr in list_tr:
        dict_tr = {
            "nom": "",
            "num": "",
            "proto": "",
            "desc": ""
        }
        list_td = tr.findAll('td')
        dict_tr["nom"] = list_td[0].text.strip()
        dict_tr["num"] = list_td[1].text.strip()
        dict_tr["proto"] = list_td[2].text.strip()
        dict_tr["desc"] = list_td[3].text.strip()
        list_data.append(dict_tr)

    # On crée le dictionnaire avec la structure attendue
    dict_json = {}
    for line in list_data:
        dict_json[line["num"]] = {}
    for line in list_data:
        if line["proto"] not in dict_json[line["num"]]:
            dict_json[line["num"]][line["proto"]] = {}
    for line in list_data:
        if line["nom"] not in dict_json[line["num"]][line["proto"]]:
            dict_json[line["num"]][line["proto"]][line["nom"]] = line["desc"]
    # print(f"dict_json : {dict_json}")
    # On vérifie l'existence de l'arborescence
    if not os.path.exists("exports/json"):
        os.makedirs("exports/json")
    # On écrit dans le fichier json les éléments de dict_json
    with open("exports/json/"+json_file_name+'.json', 'w', encoding='utf8') as jsonfile:
        json.dump(dict_json, jsonfile, indent=4)

    print(col_green + "Fichier "+json_file_name+".json créé !" + col_end)


def test_cnx(url_cnx):
    # On récupère le contenu de la page en cours avec gestion des erreurs
    try:
        req_test = requests.get(url_cnx)
    except requests.ConnectionError as er:
        print(col_red+"\nErreur : Vérifiez votre connexion à Internet."+col_end)
        print(str(er))
        return False
    except requests.Timeout as er:
        print(col_red+"Erreur : Timeout."+col_end)
        print(str(er))
        return False
    except requests.RequestException as er:
        print(col_red+"Erreur générale."+col_end)
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
