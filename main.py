import requests
import bs4
import scraper
import base64
from datetime import datetime
import time
import dearpygui.dearpygui as dpg
import sys
import os
import re


# Indispensable pour auto-py-to-exe en mode 1 fichier
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # print(base_path)
    return os.path.join(base_path, relative_path)


url = 'https://www.frameip.com/liste-des-ports-tcp-udp/'
list_titre = []
list_b = []
list_tr = []
list_p = []
list_a = []
list_elem = []
b = ''
# Pour les couleurs cf : https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
# Ne fonctionne que sous Windows, pour être portable, utiliser une bibliothèque dédiée
col_red = '\033[91m'
col_green = '\33[92m'
col_yellow = '\033[93m'
col_end = '\033[0m'
list_data = []
pages_to_export = [['Port de 0 à 500', 'https://www.frameip.com/liste-des-ports-tcp-udp?plage=1']]
connected = True
init = False
csv_flag = True
json_flag = False
one_file = False
btn_scrap_txt = "Scrap !"
btn_scrap_en = True
status_txt = ''
status_color = (50, 150, 255, 255)
img = [resource_path("img/led_off.png"), resource_path("img/led_green.png"), resource_path("img/led_red.png")]
now = datetime.now()


def header_callback():
    # on crée une nouvelle fenêtre pour les headers
    with dpg.window(label="", width=420, height=230, no_resize=True, pos=(35, 80), on_close=exit_popup, modal=True,
                    tag="header_window", horizontal_scrollbar=True):
        dpg.add_group(tag="grp_headers")
    # on récupère les headers
    headers = scraper.read_headers(url)
    # on affiche les headers dans la fenêtre
    for line in headers:
        dpg.add_text(line + " : " + headers[line], parent="grp_headers")


def cookies_callback():
    with dpg.window(label="", width=420, height=230, no_resize=True, pos=(35, 80), on_close=exit_popup, modal=True,
                    tag="cookies_window", horizontal_scrollbar=True):
        dpg.add_group(tag="grp_cookies")
        # on récupère les cookies
        cook = scraper.cookies(url)
        print(url)
        if cook:
            for line in cook:
                dpg.add_text(line.name + " : " + line.value, parent="grp_cookies")
        else:
            dpg.add_text("Ce site ne comporte aucun cookie \n\n(Il respecte votre vie privée !)",
                         color=(0, 255, 0, 255), parent="grp_cookies")


def custom_cookies_callback():
    with dpg.window(label="", width=420, height=230, no_resize=True, pos=(35, 80), on_close=exit_popup, modal=True,
                    tag="custom_cookies_window", horizontal_scrollbar=True):
        dpg.add_text("Entrer une url pour y chercher des cookies", color=(255, 255, 0, 255))
        dpg.add_group(tag="grp_cust_cookies")
        dpg.add_group(tag="grp_cust_cookies_inp", parent="grp_cust_cookies", horizontal=True, horizontal_spacing=10)
        dpg.add_text("URL :", parent="grp_cust_cookies_inp")
        cust_cookies_url_input = dpg.add_input_text(tag="cust_cookies_url_input", parent="grp_cust_cookies_inp",
                                                    default_value="https://www.google.com",
                                                    width=320, hint="https://www.google.com")
        dpg.add_button(tag="get_cust_cookies", label="ok",
                       width=26, height=20, parent="grp_cust_cookies_inp",
                       callback=get_custom_cookies_callback, user_data=dpg.get_value(cust_cookies_url_input))
        dpg.add_group(tag="grp_cust_cookies_res", parent="grp_cust_cookies")


def get_custom_cookies_callback():
    url_c = dpg.get_value("cust_cookies_url_input")
    # print(url_c)
    # On vérifie si l'url saisie est correctement formatée
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9() \
                  @:%_\\+.~#?&\\/=]*)$"
    if not re.match(url_pattern, url_c):  # Returns Match object
        dpg.delete_item("grp_cust_cookies_res", children_only=True)
        dpg.add_text("Erreur : Vérifiez l'url saisie...", tag="err_txt", parent="grp_cust_cookies_res", color=(255, 0, 0, 255))
    else:
        # on récupère les cookies
        cook = scraper.cookies(url_c)
        dpg.delete_item("grp_cust_cookies_res", children_only=True)
        if cook:
            dpg.add_text("Cookies trouvés :", parent="grp_cust_cookies_res", color=(255, 0, 0, 255))
            for line in cook:
                dpg.add_text(line.name + " : " + line.value, parent="grp_cust_cookies_res")
        else:
            dpg.add_text("Ce site ne comporte aucun cookie \n\n(Il respecte votre vie privée !)",
                         color=(0, 255, 0, 255), parent="grp_cust_cookies_res")


def check_callback(sender, app_data, user_data):
    global pages_to_export
    global one_file
    if app_data:
        pages_to_export.append(user_data)
    else:
        pages_to_export.remove(user_data)
    if len(pages_to_export) == 0:
        dpg.configure_item("btn_scrap", enabled=False, label="Rien à scraper")
    else:
        dpg.configure_item("btn_scrap", enabled=True, label="Scrap !")
    if len(pages_to_export) == 9:
        dpg.configure_item("cb_one_file", show=True)
    else:
        dpg.configure_item("cb_one_file", show=False)
        dpg.set_value("cb_one_file", False)
        one_file = False


def btn_cb_all_callback():
    global pages_to_export
    cbs = dpg.get_item_children(grp_checkbox)
    pages_to_export = []
    for cb in cbs[1]:
        pages_to_export.append(dpg.get_item_user_data(cb))
        dpg.set_value(cb, True)
    dpg.configure_item("btn_scrap", enabled=True, label="Scrap !")
    dpg.configure_item("cb_one_file", show=True)


def btn_cb_none_callback():
    global pages_to_export
    global one_file
    pages_to_export = []
    cbs = dpg.get_item_children(grp_checkbox)
    for cb in cbs[1]:
        dpg.set_value(cb, False)
    dpg.configure_item("btn_scrap", enabled=False, label="Rien à scraper")
    dpg.set_value("cb_one_file", False)
    dpg.configure_item("cb_one_file", show=False)
    one_file = False


def cb_one_file_callback(sender):
    global one_file
    if sender:
        one_file = True
    else:
        one_file = False


def radio_callback(sender, app_data):
    global csv_flag
    global json_flag
    if app_data == "CSV":
        csv_flag = True
        json_flag = False
    elif app_data == "JSON":
        csv_flag = False
        json_flag = True
    else:
        csv_flag = True
        json_flag = True


def exit_popup(sender):
    dpg.delete_item(sender)


def scrap_callback():
    start = datetime.now()

    if one_file:
        with dpg.window(label="", width=240, height=100, no_resize=True, pos=(120, 80), on_close=exit_popup, modal=True):
            title_popup = dpg.add_text("Scrap dans 1 fichier en cours...", tag="title_popup")
            dpg.add_loading_indicator(tag="load", pos=(100, 50))
        scraper.scrap(pages_to_export, csv_flag, json_flag, True)
        time.sleep(5)
        dpg.delete_item("load")
    else:
        # On crée une fenêtre pour afficher la progression du scrap et le résultat final
        with dpg.window(label="", width=420, height=150, no_resize=True, pos=(35, 80), on_close=exit_popup, modal=True):
            title_popup = dpg.add_text("Scrap en cours...", tag="title_popup")
            pb = dpg.add_progress_bar(label="progress_bar", width=400, height=20, default_value=0)
            res_grp = dpg.add_group(tag="res_grp")
            dpg.add_text("Résultat :", parent="res_grp")
        res = " => "
        if csv_flag:
            res += ".csv "
        if json_flag:
            res += ".json "
        pg_val = 0.0
        step = 1 / len(pages_to_export)
        for page in pages_to_export:
            # la barre de progression est mise à jour en fonction de la progression du scrap
            dpg.set_value(title_popup, page[1])
            dpg.configure_item(title_popup, color=(50, 150, 255, 255))
            dpg.configure_item(pb, show=True)
            dpg.configure_item(pb, overlay=str(int(pg_val * 100)) + "%")
            pg_val += step
            dpg.add_text(page[0] + res, parent=res_grp)
            # name = page[0].replace(" ", "_")
            scraper.scrap([page], csv_flag, json_flag, False)
            dpg.set_value(pb, value=pg_val)
            dpg.render_dearpygui_frame()
        dpg.configure_item(pb, overlay="100%")
        dpg.render_dearpygui_frame()
    elapsed = datetime.now() - start
    dpg.set_value(title_popup, f"Scrap terminé en {int(elapsed.total_seconds())}s !")
    dpg.configure_item(title_popup, color=(0, 255, 0, 255))


def test_cnx_callback(sender, app_data, user_data):
    global connected
    global links
    global init
    global one_file

    test_return = scraper.test_cnx(url)
    cb_now = datetime.now()

    if test_return and not connected:  # Si connecté avant mais plus maintenant
        cb_req = requests.get(url)
        cb_uls = bs4.BeautifulSoup(cb_req.content, "html.parser").findAll("ul")
        cb_ul = cb_uls[1]
        links = cb_ul.findAll('a')
        dpg.set_value(led_tex, user_data['textures'][1])
        dpg.configure_item(status_bar_txt,
                           default_value="OK, connexion avec le site établie à " + now.strftime("%H:%M:%S"))
        dpg.configure_item(status_bar_txt, color=(0, 255, 0, 255))
        if init:
            dpg.configure_item(grp_checkbox, show=True)
        else:  # Le prog a été démarré sans connexion au site, il faut créer les checkbox
            dpg.configure_item(grp_checkbox, show=True)
            first_only = 0
            # print(f"LINKS={links}")
            for cb_link in links:
                # On sélectionne la 1ère page par défaut
                if first_only == 0:
                    dpg.add_checkbox(label=cb_link.text, tag=cb_link['href'], callback=check_callback,
                                     parent="grp_checkbox", default_value=True)
                else:
                    dpg.add_checkbox(label=cb_link.text, tag=cb_link['href'], callback=check_callback,
                                     parent="grp_checkbox")
                first_only += 1
        dpg.configure_item(btn_scrap, enabled=True, label="Scrap !")
        dpg.configure_item(btn_header, show=True)
        dpg.configure_item(btn_cookie, show=True)
        dpg.configure_item(btn_cust_cookie, show=True)
        dpg.configure_item(btn_cb_all, show=True)
        dpg.configure_item(btn_cb_none, show=True)
        if len(links) == 9:
            dpg.configure_item(cb_one_file, show=True)
        connected = True
        init = True
        # print("TEST_CNX_CALLBACK-1 INIT="+str(init))
    elif test_return and connected:  # Si déjà connecté avant et toujours connecté
        dpg.configure_item(status_bar_txt, color=(0, 255, 0, 255),
                           default_value="OK, connexion avec le site toujours établie à " + cb_now.strftime("%H:%M:%S"))
        # print("TEST_CNX_CALLBACK-2 INIT="+str(init))
    else:  # Si pas connecté
        dpg.set_value(led_tex, user_data['textures'][2])
        dpg.configure_item(status_bar_txt, color=(255, 0, 0, 255),
                           default_value="Erreur, la connexion avec le site a échoué à " + cb_now.strftime("%H:%M:%S"))
        dpg.configure_item(btn_scrap, enabled=False, label="Rien à scraper")
        dpg.configure_item(grp_checkbox, show=False)
        dpg.configure_item(btn_header, show=False)
        dpg.configure_item(btn_cookie, show=False)
        dpg.configure_item(btn_cust_cookie, show=False)
        dpg.configure_item(btn_cb_all, show=False)
        dpg.configure_item(btn_cb_none, show=False)
        dpg.configure_item(cb_one_file, show=False)
        dpg.set_value(cb_one_file, False)
        one_file = False
        connected = False
        # print("TEST_CNX_CALLBACK-3 INIT="+str(init))


def dec_():
    db = base64.b64decode(b).decode('utf-8')
    dpg.get_value(status_bar_txt)
    dpg.configure_item(status_bar_txt, default_value=db, color=(255, 128, 0, 255))
    print(db)


def exit_callback():
    dpg.destroy_context()
    exit()


# player = 0
#
# while player != "y" :   # Tant que l'utilisateur joue
#
#     player = input('Êtes-vous sûr de vouloir jouer ? (y = oui, n = non) : ')
#
#     if player == "y":     # Si l'utilisateur souhaite jouer
#         print('Vous avez choisi de jouer !')
#
#     elif player == "n":   # Si l'utilisateur refuse de jouer
#         print('Vous avez choisi de ne pas jouer !')
#         exit()
#
#     else:
#         print('Erreur, vous devez écrire y ou n !')
#
# print()
# print(col_yellow + "Page à traiter : " + col_end)
# print(url)

try:
    req = requests.get(url)
except requests.ConnectionError as e:
    print(f"{col_red}\nErreur ! Vérifiez votre connexion à Internet :{col_end}")
    print(str(e))
except requests.Timeout as e:
    print(f"{col_red}\nErreur ! Timeout :{col_end}")
    print(str(e))
except requests.RequestException as e:
    print(f"{col_red}\nErreur générale :{col_end}")
    print(str(e))
except KeyboardInterrupt:
    print(f"{col_yellow}\nLe programme a été fermé.{col_end}")
except Exception as e:
    print("Erreur inconnue !" + str(e))

# On parse le html avec BeautifulSoup
try:
    uls = bs4.BeautifulSoup(req.content, "html.parser").findAll("ul")
    ul = uls[1]
    links = ul.findAll('a')
except Exception as ex:
    print(ex)
    links = []

# DearPyGuy Interface ####################################
dpg.create_context()

# Création des images
dic_tex = {}
for i in range(len(img)):
    width, height, channels, data = dpg.load_image(img[i])
    with dpg.texture_registry():
        dic_tex[i] = data
img_handler_dict = {
    'key': 1,
    'textures': dic_tex
}
led_img = img[0]
width, height, channels, data = dpg.load_image(led_img)
with dpg.texture_registry():
    led_tex_off = dpg.add_dynamic_texture(width, height, data)
led_tex = led_tex_off

# On vérifie la connexion avant de construire l'interface graphique
# (On ne peut pas récupérer les liens - checkbox - sans connexion)
if scraper.test_cnx(url) and not init:
    led_img = img[1]
    width, height, channels, data = dpg.load_image(led_img)
    with dpg.texture_registry():
        led_tex_green = dpg.add_dynamic_texture(width, height, data)
    status_txt = "OK, connexion avec le site établie"
    status_color = (0, 255, 0, 255)
    led_tex = led_tex_green
    btn_scrap_txt = "Scrap !"
    btn_scrap_en = True
    btn_head_cook_show = True
    btn_cb_show = True
    connected = True
    init = True
    # print("TEST_CNX-1 INIT=" + str(init))
else:
    led_img = img[2]
    width, height, channels, data = dpg.load_image(led_img)
    with dpg.texture_registry():
        led_tex_red = dpg.add_dynamic_texture(width, height, data)
    status_txt = "Erreur, la connexion avec le site a échoué"
    status_color = (255, 0, 0, 255)
    led_tex = led_tex_red
    btn_scrap_txt = "Rien à scraper"
    btn_scrap_en = False
    btn_head_cook_show = False
    btn_cb_show = False
    connected = False
    init = False
    # print("TEST_CNX-2 INIT="+str(init))

# Construction de l'interface graphique
# On affecte une variable à chaque contrôle qu'on aura à modifier ultérieurement
# Pas besoin de spécifier d'attributs à window si elle est désignée en "primary window"
with dpg.window(tag="prim_win"):
    dpg.add_text(default_value="Page web : " + url, color=(50, 150, 255, 255))
    dpg.add_image(pos=(455, 9), texture_tag=led_tex, tag="led")
    dpg.add_button(pos=(-3, 9), callback=dec_, user_data=b)
    with dpg.drawlist(width=500, height=10):
        dpg.draw_line((0, 5), (470, 5), color=(60, 60, 60, 255), thickness=1)
    grp_grp_cb = dpg.add_group(tag="grp_grp_cb", horizontal=True)
    dpg.add_drawlist(width=10, height=205, parent="grp_grp_cb")
    grp_checkbox = dpg.add_group(tag="grp_checkbox", parent="grp_grp_cb")
    n = 0
    all_pages = {}
    for link in links:
        label = link.text
        href = link['href']
        if n == 0:
            dpg.add_checkbox(label=label, tag=href, callback=check_callback, parent="grp_checkbox",
                             user_data=[label, href], default_value=True)
        else:
            dpg.add_checkbox(label=label, tag=href, callback=check_callback, parent="grp_checkbox",
                             user_data=[label, href])
        n += 1
    dpg.add_group(tag="grp_grp_btn", parent="grp_grp_cb")
    dpg.add_drawlist(width=200, height=16, parent="grp_grp_btn")
    btn_header = dpg.add_button(label="Afficher les headers",
                                callback=header_callback,
                                tag="btn_headers",
                                width=150, height=50,
                                parent="grp_grp_btn",
                                indent=70,
                                show=btn_head_cook_show)
    dpg.add_drawlist(width=200, height=10, parent="grp_grp_btn")
    btn_cookie = dpg.add_button(label="Afficher les cookies",
                                callback=cookies_callback,
                                tag="btn_cookies",
                                width=150, height=50,
                                parent="grp_grp_btn",
                                indent=70,
                                show=btn_head_cook_show)
    dpg.add_drawlist(width=200, height=10, parent="grp_grp_btn")
    btn_cust_cookie = dpg.add_button(label="Afficher les cookies\n\n   d'un autre site",
                                     callback=custom_cookies_callback,
                                     tag="btn_cust_cookies",
                                     width=150, height=50,
                                     parent="grp_grp_btn",
                                     indent=70,
                                     show=btn_head_cook_show)
    grp_cb_btn = dpg.add_group(tag="grp_cb_btn", horizontal=True, horizontal_spacing=10)
    dpg.add_drawlist(width=0, height=17, parent="grp_cb_btn")
    btn_cb_all = dpg.add_button(label="Tous", tag="btn_cb_all", indent=18, width=40, height=20,
                                parent="grp_cb_btn", show=btn_cb_show, callback=btn_cb_all_callback)
    btn_cb_none = dpg.add_button(label="Aucun", tag="btn_cb_none", width=40, height=20,
                                 parent="grp_cb_btn", show=btn_cb_show, callback=btn_cb_none_callback)
    cb_one_file = dpg.add_checkbox(label="1 seul fichier", tag="cb_one_file",
                                   callback=cb_one_file_callback, parent="grp_cb_btn", show=False)
    with dpg.drawlist(width=500, height=30):
        dpg.draw_line((0, 5), (470, 5), color=(255, 0, 0, 255), thickness=1)
    dpg.add_radio_button(items=["CSV", "JSON", "CSV & JSON"],
                         label="Choix de la sortie",
                         tag="rb_output",
                         callback=radio_callback,
                         horizontal=True,
                         indent=130)
    with dpg.drawlist(width=500, height=35, pos=(0, 480)):
        dpg.draw_line((0, 25), (470, 25), color=(255, 0, 0, 255), thickness=1)
    dpg.add_group(tag="main_buttons", horizontal=True, horizontal_spacing=10)
    dpg.add_button(
        label="Test connexion",
        tag="btn_test_cnx",
        callback=test_cnx_callback,
        user_data=img_handler_dict,
        width=150, height=50,
        parent="main_buttons")
    with dpg.tooltip("btn_test_cnx"):
        dpg.add_text("Tester la connexion avec le site")
    btn_scrap = dpg.add_button(
        label=btn_scrap_txt,
        tag="btn_scrap",
        callback=scrap_callback,
        width=150, height=50,
        parent="main_buttons",
        enabled=btn_scrap_en)
    with dpg.tooltip("btn_scrap"):
        dpg.add_text("Démarrer le scrap des pages sélectionnées")
    dpg.add_button(
        label="Exit",
        tag="btn_exit",
        callback=exit_callback,
        width=150, height=50,
        parent="main_buttons")
    with dpg.tooltip("btn_exit"):
        dpg.add_text("Quitter le programme")
    with dpg.drawlist(width=500, height=11):
        dpg.draw_line((0, 10), (470, 10), color=(60, 60, 60, 255), thickness=1)
    status_bar_txt = dpg.add_text(tag="status_bar_txt", default_value=status_txt, color=status_color)

# PROGRESS ########################################################################################
# i = 0.0
# while i < 1.0:
#     # On affiche la barre de progression que si l'on clique sur le bouton "Scrap"
#     dpg.set_value("progress", i)
#     i += 0.01
#     dpg.render_dearpygui_frame()
# dpg.set_value("progress", 1.0)
# dpg.render_dearpygui_frame()
# dpg.add_progress_bar(id="progress", overlay="Vérification de la connection ...", default_value=0)
# /PROGRESS #######################################################################################

# Thème perso
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    # with dpg.theme_component(dpg.mvInputInt):
    # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core)
    # dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
dpg.bind_theme(global_theme)
# dpg.show_style_editor()

# Viewport (fenêtre de l'OS - conteneur principal) et initialisations de l'interface graphique
b = 'T24gbmHDrnQgdG91cyDDqWdhdXgsIG1haXMgY2VydGFpbnMgcGx1cyBxdWUgZCdhdXRyZXMuLi4='
dpg.create_viewport(title='ScrapPy v0.1.42 beta={Tp3: ["by", "Bryan", "&", "Olivier"]}',
                    width=500, height=510, resizable=False, vsync=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("prim_win", True)
# Démarrage de la boucle de refresh
dpg.start_dearpygui()
# while dpg.is_dearpygui_running():  # Idem
#     # put old render callback code here!
#     dpg.render_dearpygui_frame()
dpg.destroy_context()
