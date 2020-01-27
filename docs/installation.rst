============
INSTALLATION
============
.. image:: http://geonature.fr/img/logo-pne.jpg
    :target: http://www.ecrins-parcnational.fr

Création de la base de données PostgreSQL
=========================================


Modification du fichier de configuration
----------------------------------------

* Créer le fichier de configuration à partir du template 'settings.ini.tpl'

::
    cp settings.ini.tpl settings.ini
::


* Ajouter les informations dans le fichier settings.ini pour se connecter à la base de données fraichement créée



Création de la base de données 'followdem' et du schéma 'utilisateur'
---------------------------------------------------------------------

* Rendre le fichier exécutable 'install.dh'

::
    chmod +x ./install_db.sh
::


* Lancer le script d'Installation

::
    ./install_db.sh
::



Création du schéma et des tables followdem
------------------------------------------

::
    export FLASK_APP=app.py
::

* Mettre à jour la base d edonnées

::
    flask db upgrade
::


* Lancer l'application

```
flask run

```