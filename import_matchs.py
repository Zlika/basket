#!/usr/bin/env python3
# Téléchargement du fichier de matches depuis FBI et import dans Kali-sport.
# Dépendances (paquets Debian) : python3-selenium, chromium-driver
import os
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Répertoire pour enregistrer le fichier rechercherRencontre.xlsx de FBI
download_path = "/tmp"
matchs_file = download_path + "/rechercherRencontre.xlsx"

def wait_file_downloaded(filename, timeout=60):
    end_time = time.time() + timeout
    while not os.path.exists(filename):
        time.sleep(1)
        if time.time() > end_time:
            return False
    if os.path.exists(filename):
        return True

def delete_previous_matchs_file():
    if os.path.isfile(matchs_file):
        os.remove(matchs_file)

def create_web_driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Pour faire fonctionner chrome dans un conteneur docker
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    prefs = {"download.default_directory" : download_path}
    options.add_experimental_option("prefs", prefs);
    return webdriver.Chrome(options=options)

def download_matchs_file_from_fbi(driver, username_fbi, password_fbi):
    # Télécharngement du fichier rechercherRencontre.xlsx
    print("Connexion à FBI")
    driver.get("https://extranet.ffbb.com/fbi/identification.do")
    driver.find_element(By.ID, "materialLoginFormEmail").send_keys(username_fbi)
    driver.find_element(By.ID, "materialLoginFormPassword").send_keys(password_fbi)
    driver.find_element(By.CSS_SELECTOR, ".btn").click()
    try:
        driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(4) > #nav").click()
    except ElementNotInteractableException:
        driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(4) > #nav").click()
    driver.find_element(By.LINK_TEXT, "Saisie des résultats").click()
    print("Recherche des matchs")
    driver.find_element(By.ID, "rechercher").click()
    print("Export des matchs")
    WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".boutonExcelNew")))
    driver.find_element(By.CSS_SELECTOR, ".boutonExcelNew").click()
    wait_file_downloaded(matchs_file)
    print("Fin du téléchargement")

def import_matchs_file_to_kalisport(driver, url_kali, username_kali, password_kali):
    # Upload dans kalisport
    print("Connexion à Kali")
    driver.get(url_kali + "/connexion")
    driver.find_element(By.ID, "login").send_keys(username_kali)
    driver.find_element(By.ID, "mdp").send_keys(password_kali)
    driver.find_element(By.ID, "cmdOk").click()
    print("Conversion du fichier")
    driver.get("https://ese-basket-ttt.kalisport.com/private/programme/importer")
    # Refus des cookies pour faire disparaitre la bannière qui masque certains boutons
    time.sleep(1)
    driver.find_element(By.ID, "tarteaucitronAllDenied2").click()
    WebDriverWait(driver, 10).until(
            expected_conditions.invisibility_of_element_located((By.ID, 'tarteaucitronAlertBig')))
    driver.find_element(By.ID, "fichier").send_keys(matchs_file)
    driver.find_element(By.ID, "cmdImporterStep2").click()
    driver.find_element(By.ID, "cmdImporterStep3").click()
    driver.find_element(By.ID, "cmdImporterStep5").click()
    print("Import des données")
    driver.find_element(By.LINK_TEXT, "Importer le résultat de la conversion").click()
    driver.find_element(By.ID, "cmdImporterStep3").click()
    driver.find_element(By.ID, "cmdImport").click()
    WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), \"Résultat de l'import\")]")))
    print("Fin de l'import")

def main():
    if len(sys.argv) != 6:
        raise Exception("Arguments attendus : identifiant et mot de passe FBI, identifiant et mot de passe Kalisport")
    # Identifiants FBI et Kalisport
    # Le compte FBI nécessite un profil du type 'Association - Engagement',
    # 'Association' ou 'Association - Compétitions' pour accéder au fichier.
    username_fbi = sys.argv[1]
    password_fbi = sys.argv[2]
    url_kali = sys.argv[3]
    username_kali = sys.argv[4]
    password_kali = sys.argv[5]

    delete_previous_matchs_file()
    try:
        driver = create_web_driver()
        download_matchs_file_from_fbi(driver, username_fbi, password_fbi)
        import_matchs_file_to_kalisport(driver, url_kali, username_kali, password_kali)
    except Exception:
        driver.get_screenshot_as_file(download_path + "/screenshot.png")
        raise
    finally:
        driver.quit()

if __name__=="__main__":
    main()
