# Open-Medilink
Medilink ou MedilinkOS est un logiciel de gestion hospitalière poussé. Malheuresement compte tenue de la zone géographie du developpeur qui a mis plus de 2 ans pour développer ce logiciel il n'as pas put vendre les liscences de son logiciel. En éspérant que ce logiciel puisse profiter a des pays plus démunie. (Voir README pour la suite.)

MedilinkOS - Hospital Efficiency Edition

MedilinkOS est un Système d'Information Hospitalier (SIH) et un Dossier Patient Informatisé (DPI) complet, conçu pour fonctionner en local. Créé par Enzo Maisonnier, ce logiciel met l'accent sur la sécurité des données médicales, la conformité RGPD et l'efficacité du personnel soignant.

Bilingue : Interface disponible en Français et en Anglais.

Fonctionnalités Principales

Sécurité & Chiffrement (Zero-Cloud)

Fonctionnement 100% local (aucune donnée sur des serveurs tiers).

Chiffrement des données médicales et identités en AES-256 (via cryptography).

Mots de passe hachés avec Bcrypt.

Génération de clés de récupération uniques.

Mode "Privacy Shield" (Bouton discret) permettant de masquer instantanément l'écran.

Conformité RGPD & Audit

Journal d'audit inaltérable (chaînage cryptographique des logs type blockchain).

Gestion stricte du consentement patient.

Droit à l'oubli : Suppression sécurisée et écrasement physique des fichiers liés au patient.

Export de dossier au format JSON.

Dossier Patient Informatisé (DPI)

Suivi clinique, antécédents, allergies, codage CIM-10 intégré.

Constantes vitales et historique de soins.

Génération et impression d'Ordonnances et de Lettres de sortie (HTML/PDF).

Gestion et Organisation

Planning (GAP) : Prise de rendez-vous, suivi de l'état (En salle, Réalisé, etc.).

Messagerie interne sécurisée (avec balises d'urgence 🚨 et partage direct de dossiers patients).

Tableau de bord avec vue dynamique de l'occupation des lits (Cartographie du service).

Tâches (To-Do) : Suivi personnel des tâches.

Outils Médicaux Intégrés

Calcul de la Clairance de la Créatinine (Formule de Cockcroft-Gault).

Score de Glasgow.

Installation & Démarrage

Prérequis

Python 3.8 ou supérieur.

Système d'exploitation : Windows, macOS ou Linux.

1. Cloner le dépôt

git clone (https://github.com/Enzomsnr/Open-Medilink) cd MedilinkOS


2. Installer les dépendances

Il est recommandé d'utiliser un environnement virtuel (venv).

pip install -r requirements.txt


(Si vous n'avez pas de fichier requirements.txt, vous pouvez installer les paquets directement :)

pip install customtkinter bcrypt cryptography Pillow


3. Lancer l'application

python medilink.py


4. Premier Lancement

Clé d'activation : Au premier démarrage, le système vous demandera une clé. Utilisez l'une des clés standard (ex: MEDILINK-STD-ALPHA-001) ou testeur disponibles dans le code source.

Configuration : Créez le compte Administrateur/Médecin initial. Une clé de récupération vous sera fournie : gardez-la précieusement !

🛠️ Stack Technique

Interface Graphique : CustomTkinter (Interface moderne adaptée aux écrans haute résolution).

Base de Données : SQLite3 (intégrée).

Cryptographie : cryptography (Fernet, PBKDF2HMAC) et bcrypt.

Export & Impression : Génération de templates HTML + impression locale via le navigateur par défaut.

Avertissement Légal & Médical

Ce logiciel est fourni à des fins éducatives et de gestion technique.

Il ne se substitue en aucun cas au jugement clinique d'un professionnel de santé.

Le logiciel fonctionnant en réseau local, l'utilisateur est seul responsable de la sécurisation de son matériel (Antivirus, pare-feu), ainsi que de la mise en place de sauvegardes régulières (Backups). L'éditeur de MedilinkOS décline toute responsabilité en cas de perte de données ou de cyberattaque visant les infrastructures matérielles de l'utilisateur.

Contribution

Les contributions sont les bienvenues ! Pour contribuer :

Forkez le projet.

Créez une branche pour votre fonctionnalité (git checkout -b feature/IncroyableFonctionnalite).

Commitez vos changements (git commit -m 'Ajout de la nouvelle fonctionnalité').

Pushez vers la branche (git push origin feature/IncroyableFonctionnalite).

Ouvrez une Pull Request.

Licence

Ce projet est sous licence MIT - voir le fichier LICENSE.md pour plus de détails. (Note: Vous pouvez modifier la licence selon vos préférences)

Si le logiciel est vérouillé par clé d'accès vous les trouverez dans le fichier HELP.pdf.

Développé avec passion par Enzo Maisonnier (16 ans).
