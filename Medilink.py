# --- Medilink OS V8.0 : Hospital Efficiency Edition (Bilingual FR/EN) ---
# Compatible: Windows, macOS, Linux
# Version: 8.0 + Patch Conformité France (RGPD/HDS) + Privacy Shield + Multilingue
# Powered by Enzomsnr.

import customtkinter as ctk
import sqlite3
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import os
import shutil
import sys
import ctypes
import re
import hashlib
import secrets
import string
import time
from datetime import datetime, timedelta
from tkinter import messagebox, END, filedialog, simpledialog
from PIL import Image, ImageTk, ImageFilter
import webbrowser
import tempfile
import platform

# --- CONFIGURATION GLOBALE & COMPATIBILITÉ ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if sys.platform.startswith("win"):
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

APP_NAME = "MedilinkOS - Hospital Efficiency Edition"
SIGNATURE = "Powered by Enzomsnr."

# --- BASE DE DONNÉES DES CLÉS ---
STANDARD_KEYS = [
    "MEDILINK-STD-ALPHA-001", "MEDILINK-STD-BRAVO-002", "MEDILINK-STD-CHARLIE-003",
    "MEDILINK-STD-DELTA-004", "MEDILINK-STD-ECHO-005", "MEDILINK-STD-FOXTROT-006",
    "MEDILINK-STD-GOLF-007", "MEDILINK-STD-HOTEL-008", "MEDILINK-STD-INDIA-009",
    "MEDILINK-STD-JULIETT-010"
]

TESTER_KEYS = [
    "MEDILINK-TEST-KILO-101", "MEDILINK-TEST-LIMA-102", "MEDILINK-TEST-MIKE-103",
    "MEDILINK-TEST-NOVEMBER-104", "MEDILINK-TEST-OSCAR-105", "MEDILINK-TEST-PAPA-106",
    "MEDILINK-TEST-QUEBEC-107", "MEDILINK-TEST-ROMEO-108", "MEDILINK-TEST-SIERRA-109",
    "MEDILINK-TEST-TANGO-110"
]

# --- CIM-10 SIMPLIFIÉE ---
CIM10_DATA = {
    "Grippe": "J11", "Pneumonie": "J18", "Covid-19": "U07.1", "Appendicite": "K37",
    "Fracture Fémur": "S72", "AVC Ischémique": "I63", "Infarctus Myocarde": "I21",
    "Diabète Type 2": "E11", "Hypertension": "I10", "Insuffisance Cardiaque": "I50",
    "Gastro-entérite": "A09", "Migraine": "G43", "Dépression": "F32", "Asthme": "J45"
}

# --- CGU TEXT ---

CGU_TEXT = """CONDITIONS GÉNÉRALES D'UTILISATION ET DE VENTE (CGU/CGV) - MEDILINKOS

Dernière mise à jour : 26/01/2026

1. MENTIONS LÉGALES ET OBJET



Les présentes Conditions Générales (ci-après "le Contrat") régissent l'utilisation de la licence du logiciel MedilinkOS (ci-après "le Logiciel"), édité par MedilinkCorp, société FRA au capital de +100000 €, immatriculée au RCS de Paris sous le numéro NA pour le moments, dont le siège social est situé au 130 rue Baudin, Bondy (ci-après "l'Éditeur").

Le Logiciel est une solution autonome installée localement sur le matériel du Client.



2. NATURE DU SERVICE ET ABSENCE D'HÉBERGEMENT



2.1 Fonctionnement en local Le Logiciel fonctionne exclusivement en local sur le terminal (ordinateur, tablette) ou le réseau interne du Client. L'Éditeur ne stocke, n'héberge et ne traite aucune donnée personnelle ou de santé du Client sur ses propres serveurs.



2.2 Responsabilité des données En conséquence, le Client conserve la maîtrise totale et exclusive de ses données. L'Éditeur n'a techniquement aucun accès aux fichiers patients, ordonnances ou agendas gérés par le Client via le Logiciel.



3. LIMITATION DE RESPONSABILITÉ : USAGE MÉDICAL

Le Logiciel est un outil d'assistance technique. Il ne se substitue pas au jugement clinique. Le Client (professionnel de santé) reste seul responsable des décisions médicales, des diagnostics et de la vérification des ordonnances générées. L'Éditeur ne saurait être tenu responsable d'une erreur de saisie, de dosage ou d'interaction médicamenteuse.



4. SÉCURITÉ INFORMATIQUE ET CYBERATTAQUES

4.1 Responsabilité de l'environnement matériel L'Éditeur fournit le code du Logiciel. Il appartient exclusivement au Client de sécuriser l'environnement matériel et logiciel dans lequel le Logiciel est installé (antivirus, pare-feu, sécurisation du réseau Wi-Fi/Ethernet, verrouillage des terminaux).



4.2 Exonération totale en cas de piratage L'Éditeur ne pourra en aucun cas être tenu responsable en cas d'intrusion, de vol de données, de rançongiciel (ransomware) ou de tout autre acte de cybermalveillance affectant le matériel ou le réseau du Client. Le Client reconnaît que la sécurité de ses données dépend de sa propre gestion de ses équipements informatiques.



5. SAUVEGARDE ET PERTE DE DONNÉES

5.1 Absence de sauvegarde par l'Éditeur Du fait du fonctionnement local du Logiciel, l'Éditeur n'effectue aucune sauvegarde des données du Client.



5.2 Obligation de sauvegarde du Client Le Client reconnaît qu'il est de sa seule responsabilité de mettre en place une politique de sauvegarde régulière et pérenne (backups externes, NAS, disques durs chiffrés) pour se prémunir contre la perte de données, le vol ou la panne de son matériel. L'Éditeur décline toute responsabilité en cas de perte définitive de données suite à un dysfonctionnement du matériel du Client (ex: panne de l'iPad, crash du disque dur) ou une mauvaise manipulation.



6. MISES À JOUR ET MAINTENANCE

L'Éditeur peut proposer des mises à jour pour corriger des bugs ou ajouter des fonctionnalités. Il appartient au Client d'installer ces mises à jour dès leur mise à disposition. L'Éditeur ne sera pas responsable des défauts de fonctionnement dus à l'utilisation d'une version obsolète du Logiciel.



7. DONNÉES PERSONNELLES ET RGPD

7.1 Rôle des parties Dans le cadre de l'utilisation du Logiciel en local :

Le Client est le seul Responsable de Traitement.

L'Éditeur n'agit pas en tant que sous-traitant au sens du RGPD car il n'a accès a aucune données personnelles traitées par le Client.



7.2 CONFORMITÉ RGPD

Il appartient au Client de s'assurer que son utilisation du Logiciel et le stockage de ses données (notamment sur ses propres serveurs ou NAS) sont conformes aux réglementations en vigueur (RGPD, Code de la Santé Publique).



8. EXCLUSION DES DOMMAGES INDIRECTS

L'Éditeur ne pourra être tenu responsable des dommages indirects subis par le Client, tels que pertes d'exploitation, perte de clientèle, préjudice commercial ou atteinte à la réputation, quelle qu'en soit la cause.



9. PLAFOND DE RESPONSABILITÉ

En cas de condamnation de l'Éditeur pour une faute prouvée liée à un défaut intrinsèque du code du Logiciel, le montant des dommages et intérêts sera plafonné au montant payé par le Client pour la licence du Logiciel au cours des 12 derniers mois.



10. PROPRIÉTÉ INTELLECTUELLE



Le Logiciel reste la propriété exclusive de l'Éditeur. Le Client bénéficie d'une licence d'utilisation personnelle qui lui sera remise après l'achat de celle-ci, non exclusive et incessible. Toute copie, modification ou rétro-ingénierie est interdite.



11. DROIT APPLICABLE ET JURIDICTION

Le présent contrat est soumis au droit français. Tout litige relèvera de la compétence exclusive du Tribunal de Commerce de Paris.



12. TESTEURS ET UTILISATEURS GRATUITS



12.1 Utilisation à titre gratuit Le Logiciel peut être utilisé gratuitement par des testeurs ou des utilisateurs en version d'essai. Dans ce cas, l'Éditeur ne garantit pas la disponibilité, la maintenance ou le support technique. Le Client utilise le Logiciel à ses propres risques. 



12.2 Absence de garantie L'Éditeur décline toute responsabilité en cas de dysfonctionnement, perte de données ou incompatibilité lors de l'utilisation gratuite du Logiciel. Le Client reconnaît que le Logiciel est fourni "tel quel" sans aucune garantie expresse ou implicite. De plus, l'Éditeur peux demmander à tout moment la cessation de l'utilisation gratuite du Logiciel sans préavis.



13. ACCEPTATION DES CGU

En utilisant le Logiciel, le Client reconnaît avoir lu, compris et accepté les présentes Conditions Générales d'Utilisation et de Vente dans leur intégralité. Toute modification future des CGU sera notifiée au Client lors de la prochaine utilisation du Logiciel, et son utilisation continue constituera une acceptation tacite des nouvelles conditions. Toute acction allant à l'encontre des présentes CGU pourra entraîner la résiliation immédiate de la licence d'utilisation du Logiciel sans préavis ni indemnité et poura entrainer une mise en demeur saisie au Tribunaux compétant.



14. CONTACT

Pour toute question relative aux présentes CGU ou pour contacter l'Éditeur, veuillez écrire à l'adresse suivante : medilink.rdv@gmail.com



15. CRÉDITS

Le Logiciel MedilinkOS est développé par Enzo Maisonnier. Toutes les marques, logos et noms de produits sont la propriété de leurs détenteurs respectifs.



15.1 LICENCES TIERCES

Certaines bibliothèques utilisées dans le développement du Logiciel sont sous licence open source. Veuillez consulter les fichiers de licence correspondants pour plus de détails.



15.2 REMERCIEMENTS

L'Éditeur remercie la communauté open source pour ses contributions inestimables qui ont permis le développement de ce Logiciel.



15.3 DROITS RÉSERVÉS

Tous droits réservés. Aucune partie de ce document ou du Logiciel ne peut être reproduite, stockée dans un système de récupération ou transmise sous quelque forme que ce soit, électronique, mécanique, photocopie, enregistrement ou autre, sans l'autorisation écrite préalable de l'Éditeur.

"""

# --- GESTIONNAIRE DE CONFIGURATION & LICENCE ---
class ConfigManager:
    def __init__(self):
        self.local_app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        if sys.platform == "darwin": 
            self.local_app_data = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
            
        self.config_folder = os.path.join(self.local_app_data, "Medilink_Config")
        self.config_file = os.path.join(self.config_folder, "config.json")
        
        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder)
            
        self.config_data = self.load_config()
        self.data_root = self.config_data.get("data_root", self.get_default_data_path())
        self.ensure_directories()

    def get_default_data_path(self):
        return os.path.join(self.local_app_data, "Medilink_Secure_Data")

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f)

    def set_data_path(self, new_path):
        self.config_data["data_root"] = new_path
        self.save_config()
        self.data_root = new_path

    def check_license_status(self):
        lic_type = self.config_data.get("license_type", None)
        activation_date_str = self.config_data.get("activation_date", None)
        
        if not lic_type or not activation_date_str:
            return False, "Aucune licence trouvée."

        if lic_type == "STANDARD":
            return True, "Licence Standard Active"
        
        if lic_type == "TESTER":
            try:
                act_date = datetime.strptime(activation_date_str, "%Y-%m-%d")
                expiration_date = act_date + timedelta(days=14)
                days_left = (expiration_date - datetime.now()).days
                
                if days_left < 0:
                    return False, "Période d'essai de 14 jours expirée.\nVeuillez acquérir une clé Standard."
                else:
                    return True, f"Mode Testeur : {days_left} jours restants."
            except ValueError:
                return False, "Erreur de date de licence."
        
        return False, "Licence invalide."

    def activate_software(self, input_key):
        key = input_key.strip()
        lic_type = None
        
        if key in STANDARD_KEYS:
            lic_type = "STANDARD"
        elif key in TESTER_KEYS:
            lic_type = "TESTER"
        
        if lic_type:
            self.config_data["license_key_hash"] = hashlib.sha256(key.encode()).hexdigest()
            self.config_data["license_type"] = lic_type
            if "activation_date" not in self.config_data or lic_type == "STANDARD": 
                 self.config_data["activation_date"] = datetime.now().strftime("%Y-%m-%d")
            
            if lic_type == "TESTER":
                 self.config_data["activation_date"] = datetime.now().strftime("%Y-%m-%d")

            self.save_config()
            return True, lic_type
        return False, None

    def ensure_directories(self):
        if not os.path.exists(self.data_root):
            os.makedirs(self.data_root)
        
        self.db_path = os.path.join(self.data_root, "medilink_v8.0.db")
        self.key_path = os.path.join(self.data_root, "vault_v8.key")
        self.img_folder = os.path.join(self.data_root, "medical_imaging")
        self.backup_folder = os.path.join(self.data_root, "backups")
        
        if not os.path.exists(self.img_folder): os.makedirs(self.img_folder)
        if not os.path.exists(self.backup_folder): os.makedirs(self.backup_folder)

    def create_backup(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archive_name = os.path.join(self.backup_folder, f"backup_{timestamp}")
        try:
            shutil.make_archive(archive_name, 'zip', self.data_root)
            return True, f"Sauvegarde créée : {os.path.basename(archive_name)}.zip"
        except Exception as e:
            return False, str(e)

config = ConfigManager()

# --- TRADUCTION (i18n) ---
FR_TO_EN = {
    "Activation du Logiciel": "Software Activation",
    "Entrez votre clé d'activation :": "Enter your activation key:",
    "J'accepte les CGU et la Responsabilité": "I accept T&C and Responsibility",
    "Lire les CGU": "Read T&C",
    "Activer": "Activate",
    "Initialisation...": "Initializing...",
    "Vérification de l'intégrité système...": "System integrity check...",
    "Chiffrement du coffre-fort local (AES-256)...": "Local vault encryption (AES-256)...",
    "Génération des certificats de sécurité...": "Generating security certificates...",
    "Configuration de la base de données SQL...": "SQL Database configuration...",
    "Démarrage des services hospitaliers...": "Starting hospital services...",
    "Configuration terminée.": "Setup complete.",
    "Configuration Initiale": "Initial Setup",
    "Compte Administrateur (Médecin)": "Administrator Account (Doctor)",
    "Nom Complet (ex: Dr. Martin)": "Full Name (e.g. Dr. Martin)",
    "Identifiant Connexion": "Login ID",
    "Mot de Passe Fort": "Strong Password",
    "Informations Officielles (Pour Ordonnances)": "Official Info (For Prescriptions)",
    "Numéro RPPS (11 chiffres)": "RPPS Number (11 digits)",
    "Nom Cabinet / Hôpital": "Clinic / Hospital Name",
    "Adresse Complète": "Full Address",
    "Téléphone Pro": "Professional Phone",
    "Finaliser Installation": "Finalize Installation",
    "Connexion Sécurisée": "Secure Login",
    "Identifiant": "Username",
    "Mot de passe": "Password",
    "Entrer": "Login",
    "Mot de passe oublié ?": "Forgot password?",
    "Récupération d'Accès": "Access Recovery",
    "Clé de Récupération (REC-...) :": "Recovery Key (REC-...) :",
    "Nouveau Mot de Passe :": "New Password :",
    "Réinitialiser": "Reset",
    "Annuler": "Cancel",
    "Déconnexion": "Logout",
    "👁️‍🗨️ Mode Discret": "👁️‍🗨️ Privacy Mode",
    "Tableau de bord": "Dashboard",
    "Tâches (To-Do)": "Tasks (To-Do)",
    "Planning (GAP)": "Schedule (GAP)",
    "Dossiers Patients": "Patient Records",
    "Outils Médicaux": "Medical Tools",
    "Messagerie": "Messaging",
    "RDV, Facturation et IA": "Billing, AI & Appts",
    "Administration": "Administration",
    "Mes Tâches": "My Tasks",
    "RDV Aujourd'hui": "Appts Today",
    "Messages non lus": "Unread Messages",
    "🏥 Voir Plan du Service (Lits)": "🏥 View Ward Map (Beds)",
    "Flux d'activité": "Activity Feed",
    "Plan d'Occupation des Lits": "Bed Occupancy Map",
    "Chambre": "Room",
    "LIBRE": "AVAILABLE",
    "Nouvelle tâche à faire...": "New task to do...",
    "+ Ajouter": "+ Add",
    "Aucune tâche en cours.": "No pending tasks.",
    "Formule de Cockcroft-Gault": "Cockcroft-Gault Formula",
    "Âge (ans)": "Age (years)",
    "Poids (kg)": "Weight (kg)",
    "Créatinine (µmol/L)": "Creatinine (µmol/L)",
    "Sexe": "Gender",
    "Homme": "Male",
    "Femme": "Female",
    "Calculer": "Calculate",
    "Échelle de Coma de Glasgow": "Glasgow Coma Scale",
    "Ouverture des Yeux (Y)": "Eye Opening (E)",
    "Réponse Verbale (V)": "Verbal Response (V)",
    "Réponse Motrice (M)": "Motor Response (M)",
    "Gestion des Rendez-vous": "Appointment Management",
    "+ Planifier": "+ Schedule",
    "Aucun rendez-vous.": "No appointments.",
    "Messagerie Hospitalière": "Hospital Messaging",
    "Message...": "Message...",
    "Envoyer": "Send",
    "Dossiers Patients (DPI)": "Patient Records (EHR)",
    "+ Admission": "+ Admission",
    "Tous les Services": "All Departments",
    "🔍 Rechercher (Nom, IPP)...": "🔍 Search (Name, ID)...",
    "Aucun patient trouvé.": "No patient found.",
    "Accès portail Web.": "Web portal access.",
    "Ouvrir": "Open",
    "Personnel": "Staff",
    "Système": "System",
    "+ Compte": "+ Account",
    "Interface": "Interface",
    "Mode Sombre": "Dark Mode",
    "Maintenance": "Maintenance",
    "Sauvegarde ZIP": "ZIP Backup",
    "Changer Dossier": "Change Folder",
    "Langue / Language": "Language",
    "Compte Utilisateur": "User Account",
    "Profil Médical (Ordonnances)": "Medical Profile (Prescriptions)",
    "Enregistrer": "Save",
    "Droit Oubli (RGPD)": "Right to be Forgotten",
    "Générer Lettre Sortie": "Discharge Letter",
    "Partager": "Share",
    "Sauver": "Save",
    "Hospitalisation": "Hospitalization",
    "Soins": "Nursing",
    "Médical": "Medical",
    "Constantes": "Vitals",
    "Presc": "Prescriptions",
    "Bio/Img": "Labs/Imaging",
    "Nom": "Last Name",
    "Prénom": "First Name",
    "DDN (JJ/MM/AAAA)": "DOB (DD/MM/YYYY)",
    "Mutuelle": "Insurance",
    "INS / NIR (Sécu)": "Social Security No.",
    "Consentement RGPD Signé": "GDPR Consent Signed",
    "Service": "Department",
    "Mode": "Mode",
    "Régime": "Diet",
    "Isolement": "Isolation",
    "Motif Admission": "Reason for Admission",
    "Chute": "Fall Risk",
    "Douleur": "Pain Score",
    "Transmission...": "Transmission...",
    "Antécédents": "Medical History",
    "Allergies": "Allergies",
    "Codage CIM-10 :": "ICD-10 Coding :",
    "Ajouter Diagnostic": "Add Diagnosis",
    "Observation...": "Observation...",
    "Ajouter Obs": "Add Obs",
    "Médicament": "Medication",
    "Dose": "Dose",
    "Posologie": "Posology",
    "Imprimer": "Print",
    "Ajouter Doc": "Add Doc",
    "Dossier Patient": "Patient Record",
    "Langue": "Language"
}

def tr(text):
    lang = config.config_data.get("language", "FR")
    if lang == "EN":
        return FR_TO_EN.get(text, text)
    return text

# Paramètres de Sécurité
AUTO_LOGOUT_TIME_MS = 600000 
APP_PEPPER = b"MEDILINK_HOSPITAL_CORE_SECURE_SALT_V11"
KDF_ITERATIONS = 480000 # Augmenté pour conformité

# --- DONNÉES DE RÉFÉRENCE ---
SERVICES = sorted(["Urgences", "Addictologie", "Allergologie", "Anesthésiologie", "Cardiologie", "Chirurgie",
"Chirurgie ambulatoire", "Chirurgie cardiaque", "Chirurgie digestive", "Chirurgie générale",
"Chirurgie maxillo-faciale", "Chirurgie orthopédique", "Chirurgie pédiatrique", "Chirurgie plastique",
"Chirurgie thoracique", "Chirurgie vasculaire", "Dermatologie", "Endocrinologie", "Gastro-entérologie",
"Gériatrie", "Gynécologie", "Hématologie", "Hépato-gastro-entérologie", "Immunologie", "Infectiologie",
"Médecine générale", "Médecine interne", "Maternité", "Néphrologie", "Neurologie", "Nutrition", "Oncologie",
"Ophtalmologie", "ORL", "Orthopédie", "Pédiatrie", "Pneumologie", "Psychiatrie", "Radiologie", "Réanimation",
"Rhumatologie", "Soins intensifs", "Soins palliatifs", "Traumatologie", "Urologie"])

MUTUELLES = sorted(["Aucune", "ADREA Mutuelle", "AG2R La Mondiale", "Aésio Mutuelle", "Alptis", "Allianz Santé",
"April Santé", "Apivia Mutuelle", "Aon", "Assurema", "AXA Santé", "Banque Populaire Assurance"])

GROUPES_SANGUINS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
SEXES = ["Masculin", "Féminin"]
ROLES = ["admin", "medecin", "infirmier", "secretaire", "aide-soignant", "interne"]
REGIMES = ["Normal", "Sans Sel", "Diabétique", "Sans Gluten", "Hypocalorique", "Hyperprotéiné", "Mixé/Haché", "À Jeun Strict"]
MODES_ADMISSION = ["Urgences", "Programmé", "Mutation Interne", "Consultation Externe", "Transfert Hôpital"]
ISOLEMENTS = ["Aucun", "Contact", "Gouttelettes", "Air", "Protecteur (Aplasie)"]
RISQUES = ["Aucun", "Chute", "Escarre", "Fugue", "Suicide", "Agitation"]

# --- FONCTIONS UTILITAIRES ---
def open_file_windows(path):
    try:
        if sys.platform == "win32": os.startfile(path)
        elif sys.platform == "darwin": os.system(f"open '{path}'")
        else: os.system(f"xdg-open '{path}'")
    except OSError as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir : {e}")

def generate_html_report(doc_profile, title, content_html, filename_prefix="doc"):
    html_template = f"""<html><head><meta charset="utf-8"><title>{title}</title><style>
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; padding: 40px; color: #333; font-size: 12px; margin: 0; }}
        .page-container {{ width: 100%; max-width: 800px; margin: 0 auto; }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #2980b9; padding-bottom: 10px; margin-bottom: 20px; }}
        .logo-area {{ width: 50%; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #2980b9; margin-bottom: 5px; }}
        .doc-info {{ font-size: 11px; line-height: 1.4; color: #555; text-align: right; width: 50%; }}
        .content {{ line-height: 1.5; font-size: 13px; min-height: 500px; }}
        .med-item {{ border-bottom: 1px dotted #ccc; padding: 8px 0; display: flex; justify-content: space-between; }}
        .med-name {{ font-weight: bold; font-size: 14px; }}
        .signature-box {{ margin-top: 40px; float: right; width: 250px; text-align: center; }}
        .signature-line {{ border-bottom: 1px solid #333; margin-bottom: 5px; height: 50px; }}
        .legal-footer {{ margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px; font-size: 9px; color: #777; text-align: center; clear: both; page-break-inside: avoid; }}
        h2 {{ color: #2c3e50; text-transform: uppercase; letter-spacing: 1px; font-size: 18px; text-align: center; margin-bottom: 30px; text-decoration: underline; }}
        </style></head><body>
        <div class="page-container">
            <div class="header">
                <div class="logo-area">
                    <div class="logo">MEDILINKOS</div>
                    <div style="font-size: 16px; font-weight: bold; color: #2c3e50;">{doc_profile.get('hospital', 'Hôpital')}</div>
                </div>
                <div class="doc-info">
                    <strong>{doc_profile.get('name', 'Dr.')}</strong><br>
                    RPPS : {doc_profile.get('rpps', 'N/A')}<br>
                    {doc_profile.get('address', '')}<br>
                    Tel : {doc_profile.get('phone', '')}
                </div>
            </div>
            
            <div class="content">{content_html}</div>
            
            <div class="legal-footer">
                <p>Document généré par Medilink OS le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.</p>
                <p>Conformément au RGPD et au Code de la Santé Publique, ce document contient des données de santé à caractère personnel.
                Il est strictement confidentiel et soumis au secret médical. Tout usage non autorisé est passible de poursuites.</p>
            </div>
        </div>
        <script>window.print();</script></body></html>"""
    try:
        tmp_dir = tempfile.gettempdir()
        file_path = os.path.join(tmp_dir, f"{filename_prefix}_{datetime.now().strftime('%H%M%S')}.html")
        with open(file_path, "w", encoding="utf-8") as f: f.write(html_template)
        webbrowser.open(f"file://{file_path}")
    except Exception as e: messagebox.showerror("Erreur d'impression", str(e))

# --- SÉCURITÉ ---
class SecurityManager:
    def __init__(self):
        self.file_key = self.load_or_create_file_key()
        self.final_key = self.derive_final_key(self.file_key)
        self.cipher = Fernet(self.final_key)

    def load_or_create_file_key(self):
        if not os.path.exists(config.key_path):
            key = Fernet.generate_key()
            with open(config.key_path, "wb") as key_file: key_file.write(key)
        else:
            with open(config.key_path, "rb") as key_file: key = key_file.read()
        return key

    def derive_final_key(self, file_key):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=APP_PEPPER, iterations=KDF_ITERATIONS)
        return base64.urlsafe_b64encode(kdf.derive(file_key))

    def encrypt(self, data): return self.cipher.encrypt(data.encode()).decode() if data else ""
    def decrypt(self, token):
        try: return self.cipher.decrypt(token.encode()).decode() if token else ""
        except: return ""

    def hash_password(self, password): return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    def check_password(self, password, hashed): return bcrypt.checkpw(password.encode(), hashed)
    
    def validate_password_strength(self, password):
        if len(password) < 8: return False, "Min 8 caractères."
        if not re.search(r"[0-9]", password): return False, "Doit contenir un chiffre."
        if not re.search(r"[A-Z]", password): return False, "Doit contenir une majuscule."
        return True, ""

    def generate_recovery_key(self):
        alphabet = string.ascii_uppercase + string.digits
        return '-'.join([''.join(secrets.choice(alphabet) for _ in range(4)) for _ in range(4)])

sec_manager = SecurityManager()

# --- BASE DE DONNÉES ---
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(config.db_path, timeout=10)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password BLOB, role TEXT, full_name TEXT, recovery_key_hash BLOB)''')
        
        try: self.cursor.execute("ALTER TABLE users ADD COLUMN rpps TEXT DEFAULT ''")
        except: pass
        try: self.cursor.execute("ALTER TABLE users ADD COLUMN hospital TEXT DEFAULT ''")
        except: pass
        try: self.cursor.execute("ALTER TABLE users ADD COLUMN address TEXT DEFAULT ''")
        except: pass
        try: self.cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT DEFAULT ''")
        except: pass

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, ipp TEXT UNIQUE, encrypted_identity TEXT, encrypted_medical_data TEXT, service TEXT, encrypted_ins TEXT DEFAULT '', consent_given INTEGER DEFAULT 0, consent_date TEXT DEFAULT '')''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, patient_id INTEGER, filepath TEXT, description TEXT, date_added TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS analyses (id INTEGER PRIMARY KEY, patient_id INTEGER, type TEXT, date_analysis TEXT, result_path TEXT)''') 
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS activities (id INTEGER PRIMARY KEY, user_id INTEGER, action TEXT, timestamp TEXT, FOREIGN KEY(user_id) REFERENCES users(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender_id INTEGER, recipient_id INTEGER, content TEXT, timestamp TEXT, read INTEGER DEFAULT 0, is_urgent INTEGER DEFAULT 0)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, patient_id INTEGER, doctor_id INTEGER, date_time TEXT, purpose TEXT, status TEXT, duration INTEGER DEFAULT 15, room TEXT DEFAULT '')''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT, status INTEGER DEFAULT 0, created_at TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, user_id INTEGER, action_type TEXT, details TEXT, timestamp TEXT, prev_hash TEXT, curr_hash TEXT)''')
        
        self.conn.commit()

    def is_first_run(self):
        self.cursor.execute("SELECT count(*) FROM users")
        return self.cursor.fetchone()[0] == 0

    def log_audit(self, user_id, action, details=""):
        self.cursor.execute("SELECT curr_hash FROM audit_logs ORDER BY id DESC LIMIT 1")
        last = self.cursor.fetchone()
        prev_hash = last[0] if last else "GENESIS_BLOCK"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        raw_data = f"{user_id}{action}{details}{timestamp}{prev_hash}"
        curr_hash = hashlib.sha256(raw_data.encode()).hexdigest()
        self.cursor.execute("INSERT INTO audit_logs (user_id, action_type, details, timestamp, prev_hash, curr_hash) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, action, details, timestamp, prev_hash, curr_hash))
        self.conn.commit()

    def create_user(self, username, password, role, full_name):
        is_valid, msg = sec_manager.validate_password_strength(password)
        if not is_valid: raise ValueError(msg)
        hashed = sec_manager.hash_password(password)
        recovery_key_plain = "REC-" + sec_manager.generate_recovery_key()
        recovery_hash = sec_manager.hash_password(recovery_key_plain)
        try:
            self.cursor.execute("INSERT INTO users (username, password, role, full_name, recovery_key_hash) VALUES (?, ?, ?, ?, ?)", 
                                (username, hashed, role, full_name, recovery_hash))
            self.conn.commit()
            return True, recovery_key_plain
        except sqlite3.IntegrityError: return False, None

    def update_user_details(self, username, rpps, hospital, address, phone):
        self.cursor.execute("UPDATE users SET rpps=?, hospital=?, address=?, phone=? WHERE username=?", 
                            (rpps, hospital, address, phone, username))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def get_users(self):
        self.cursor.execute("SELECT id, username, full_name, role FROM users ORDER BY full_name")
        return self.cursor.fetchall()
    
    def get_user_by_id(self, uid):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (uid,))
        return self.cursor.fetchone()

    def update_user(self, uid, username, password, role, full_name, rpps, hospital, address, phone):
        if password:
            hashed = sec_manager.hash_password(password)
            self.cursor.execute("UPDATE users SET username=?, password=?, role=?, full_name=?, rpps=?, hospital=?, address=?, phone=? WHERE id=?", 
                                (username, hashed, role, full_name, rpps, hospital, address, phone, uid))
        else:
            self.cursor.execute("UPDATE users SET username=?, role=?, full_name=?, rpps=?, hospital=?, address=?, phone=? WHERE id=?", 
                                (username, role, full_name, rpps, hospital, address, phone, uid))
        self.conn.commit()

    def delete_user(self, uid):
        self.cursor.execute("DELETE FROM users WHERE id=?", (uid,))
        self.conn.commit()

    def verify_recovery_key(self, username, input_key):
        self.cursor.execute("SELECT recovery_key_hash FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return sec_manager.check_password(input_key, result[0])
        return False

    def reset_password(self, username, new_password):
        is_valid, msg = sec_manager.validate_password_strength(new_password)
        if not is_valid: raise ValueError(msg)
        hashed = sec_manager.hash_password(new_password)
        self.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed, username))
        self.conn.commit()

    def get_patients(self):
        self.cursor.execute("SELECT id, ipp, encrypted_identity, service FROM patients")
        res = []
        for r in self.cursor.fetchall():
            try:
                ident = json.loads(sec_manager.decrypt(r[2]))
                res.append({"id": r[0], "ipp": r[1], "nom": ident.get("nom", "?"), "prenom": ident.get("prenom", "?"), "service": r[3], "h_chambre": ident.get("h_chambre", "?")})
            except: pass
        return res

    def get_patient_count(self): 
        self.cursor.execute("SELECT COUNT(id) FROM patients")
        return self.cursor.fetchone()[0]

    def save_patient(self, user_id, pid, ipp, identity, medical, service, ins, consent_given):
        enc_id = sec_manager.encrypt(json.dumps(identity))
        enc_med = sec_manager.encrypt(json.dumps(medical))
        enc_ins = sec_manager.encrypt(ins)
        
        consent_int = 1 if consent_given else 0
        consent_date = datetime.now().strftime("%Y-%m-%d") if consent_given else ""

        if pid:
            self.cursor.execute("UPDATE patients SET ipp=?, encrypted_identity=?, encrypted_medical_data=?, service=?, encrypted_ins=?, consent_given=?, consent_date=? WHERE id=?", 
                                (ipp, enc_id, enc_med, service, enc_ins, consent_int, consent_date, pid))
            self.log_audit(user_id, "UPDATE_PATIENT", f"IPP: {ipp}")
        else:
            self.cursor.execute("INSERT INTO patients (ipp, encrypted_identity, encrypted_medical_data, service, encrypted_ins, consent_given, consent_date) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                (ipp, enc_id, enc_med, service, enc_ins, consent_int, consent_date))
            self.log_audit(user_id, "CREATE_PATIENT", f"IPP: {ipp}")
        
        self.conn.commit()
        return pid if pid else self.cursor.lastrowid

    def get_full_patient(self, pid, user_id):
        self.cursor.execute("SELECT * FROM patients WHERE id=?", (pid,))
        r = self.cursor.fetchone()
        if r: 
            self.log_audit(user_id, "ACCESS_PATIENT", f"ID: {pid}")
            return {
                "id": r[0], "ipp": r[1], 
                "identity": json.loads(sec_manager.decrypt(r[2])), 
                "medical": json.loads(sec_manager.decrypt(r[3])), 
                "service": r[4],
                "ins": sec_manager.decrypt(r[5]),
                "consent": r[6]
            }
        return None

    def delete_patient_securely(self, pid, user_id):
        self.cursor.execute("SELECT filepath FROM images WHERE patient_id=?", (pid,))
        images = self.cursor.fetchall()
        for img in images:
            path = img[0]
            if os.path.exists(path):
                try:
                    file_size = os.path.getsize(path)
                    with open(path, "wb") as f: f.write(os.urandom(file_size))
                    os.remove(path)
                except: pass
        self.cursor.execute("DELETE FROM images WHERE patient_id=?", (pid,))
        self.cursor.execute("DELETE FROM appointments WHERE patient_id=?", (pid,))
        self.cursor.execute("DELETE FROM patients WHERE id=?", (pid,))
        self.log_audit(user_id, "DELETE_PATIENT", f"Right to be Forgotten ID: {pid}")
        self.conn.commit()

    def add_image(self, pid, path, desc):
        self.cursor.execute("INSERT INTO images (patient_id, filepath, description, date_added) VALUES (?, ?, ?, ?)", (pid, path, desc, datetime.now().strftime("%d/%m/%Y %H:%M")))
        self.conn.commit()

    def get_images(self, pid):
        self.cursor.execute("SELECT * FROM images WHERE patient_id=?", (pid,))
        return self.cursor.fetchall()

    def add_analysis_result(self, pid, type_name, date_ana, path):
        self.cursor.execute("INSERT INTO analyses (patient_id, type, date_analysis, result_path) VALUES (?, ?, ?, ?)", (pid, type_name, date_ana, path))
        self.conn.commit()

    def get_analysis_results(self, pid):
        self.cursor.execute("SELECT * FROM analyses WHERE patient_id=?", (pid,))
        return self.cursor.fetchall()

    def send_message(self, sender_id, recipient_id, content, is_urgent=0):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO messages (sender_id, recipient_id, content, timestamp, is_urgent) VALUES (?, ?, ?, ?, ?)", (sender_id, recipient_id, content, ts, is_urgent))
        self.conn.commit()

    def get_messages(self, user_id, other_id):
        self.cursor.execute("""
            SELECT sender_id, content, timestamp, read, is_urgent FROM messages 
            WHERE (sender_id=? AND recipient_id=?) OR (sender_id=? AND recipient_id=?)
            ORDER BY timestamp ASC
        """, (user_id, other_id, other_id, user_id))
        return self.cursor.fetchall()

    def mark_messages_read(self, user_id, sender_id):
        self.cursor.execute("UPDATE messages SET read=1 WHERE recipient_id=? AND sender_id=? AND read=0", (user_id, sender_id))
        self.conn.commit()

    def get_unread_count(self, user_id):
        self.cursor.execute("SELECT COUNT(*) FROM messages WHERE recipient_id=? AND read=0", (user_id,))
        return self.cursor.fetchone()[0]

    def add_appointment(self, patient_id, doctor_id, date_time, purpose, duration, room):
        self.cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date_time, purpose, status, duration, room) VALUES (?, ?, ?, ?, 'Prévu', ?, ?)", 
                            (patient_id, doctor_id, date_time, purpose, duration, room))
        self.conn.commit()

    def get_appointments(self, doctor_id=None, date_filter=None):
        query = "SELECT a.id, p.encrypted_identity, a.date_time, a.purpose, u.full_name, a.status, a.duration, a.room, a.patient_id FROM appointments a JOIN patients p ON a.patient_id = p.id JOIN users u ON a.doctor_id = u.id"
        args = []
        conditions = []
        if doctor_id:
            conditions.append("a.doctor_id = ?")
            args.append(doctor_id)
        if date_filter:
            conditions.append("a.date_time LIKE ?")
            args.append(f"{date_filter}%")
        if conditions: query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY a.date_time"
        
        self.cursor.execute(query, args)
        res = []
        for r in self.cursor.fetchall():
            try:
                ident = json.loads(sec_manager.decrypt(r[1]))
                res.append({"id": r[0], "patient": f"{ident['nom']} {ident['prenom']}", "date": r[2], "purpose": r[3], "doctor": r[4], "status": r[5], "duration": r[6], "room": r[7], "pid": r[8]})
            except: pass
        return res
    
    def update_appointment_status(self, app_id, new_status):
        self.cursor.execute("UPDATE appointments SET status=? WHERE id=?", (new_status, app_id))
        self.conn.commit()

    def delete_appointment(self, app_id):
        self.cursor.execute("DELETE FROM appointments WHERE id=?", (app_id,))
        self.conn.commit()

    def add_task(self, user_id, content):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO tasks (user_id, content, status, created_at) VALUES (?, ?, 0, ?)", (user_id, content, ts))
        self.conn.commit()

    def get_tasks(self, user_id):
        self.cursor.execute("SELECT id, content, status FROM tasks WHERE user_id=? ORDER BY status ASC, created_at DESC", (user_id,))
        return self.cursor.fetchall()

    def update_task_status(self, tid, status):
        self.cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, tid))
        self.conn.commit()

    def delete_task(self, tid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (tid,))
        self.conn.commit()

    def log_activity(self, user_id, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO activities (user_id, action, timestamp) VALUES (?, ?, ?)", (user_id, action, timestamp))
        self.conn.commit()

    def get_recent_activities(self, limit=8):
        self.cursor.execute("SELECT a.action, a.timestamp, u.full_name FROM activities a JOIN users u ON a.user_id = u.id ORDER BY a.timestamp DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

db = Database()

# --- UI COMPONENTS ---
class MacCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=12, fg_color=("white", "#2b2b2b"), border_color=("gray90", "gray30"), border_width=1, **kwargs)

class SectionTitle(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master, text=text, font=("SF Pro Display", 16, "bold"), anchor="w", text_color=("#34495e", "#ecf0f1"))

# --- LOGIN ---
class LoginWindow(ctk.CTk): 
    relaunch_needed = True 
    def __init__(self):
        super().__init__()
        self.title("MedilinkOS - Authentication")
        self.geometry("900x600")
        self.resizable(False, False)
        x = (self.winfo_screenwidth() - 900) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"900x600+{x}+{y}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing) 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#2c3e50")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.left_frame, text="Medilink\nHospital", font=("Helvetica", 42, "bold"), text_color="white").place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(self.left_frame, text=SIGNATURE, font=("Helvetica", 14), text_color="#bdc3c7").place(relx=0.5, rely=0.60, anchor="center")
        
        # Sélecteur de Langue
        self.lang_var = ctk.StringVar(value=config.config_data.get("language", "FR"))
        self.lang_menu = ctk.CTkOptionMenu(self.left_frame, values=["FR", "EN"], variable=self.lang_var, command=self.change_lang, width=80)
        self.lang_menu.place(relx=0.1, rely=0.9, anchor="w")

        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray98", "#1a1a1a"))
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.logged_in_user = None 
        
        is_active, msg = config.check_license_status()
        if not is_active and "Aucune licence" in msg:
            self.show_activation_screen()
        elif not is_active:
            messagebox.showerror("Licence", msg)
            self.show_activation_screen()
        elif db.is_first_run():
            self.show_first_run_setup()
        else:
            self.show_login()

    def change_lang(self, choice):
        config.config_data["language"] = choice
        config.save_config()
        self.destroy()
        LoginWindow.relaunch_needed = True
            
    def on_closing(self):
        LoginWindow.relaunch_needed = False
        self.destroy()

    def clear_right(self):
        for w in self.right_frame.winfo_children(): w.destroy()

    def show_activation_screen(self):
        self.clear_right()
        c = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        c.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(c, text=tr("Activation du Logiciel"), font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(c, text=tr("Entrez votre clé d'activation :"), text_color="gray").pack(pady=5)
        self.key_entry = ctk.CTkEntry(c, placeholder_text="MEDILINK-XXX-XXXX-000", width=280, justify="center")
        self.key_entry.pack(pady=15)
        
        self.cgu_var = ctk.BooleanVar()
        ctk.CTkCheckBox(c, text=tr("J'accepte les CGU et la Responsabilité"), variable=self.cgu_var).pack(pady=10)
        ctk.CTkButton(c, text=tr("Lire les CGU"), fg_color="gray", command=self.show_cgu_text).pack(pady=5)
        ctk.CTkButton(c, text=tr("Activer"), width=280, height=40, fg_color="#27ae60", command=self.do_activation).pack(pady=20)

    def show_cgu_text(self):
        t = ctk.CTkToplevel(self)
        t.title("CGU")
        t.geometry("500x600")
        ctk.CTkLabel(t, text="Conditions Générales d'Utilisation", font=("Arial", 16, "bold")).pack(pady=10)
        box = ctk.CTkTextbox(t)
        box.pack(fill="both", expand=True, padx=10, pady=10)
        box.insert("1.0", CGU_TEXT)
        box.configure(state="disabled")

    def do_activation(self):
        if not self.cgu_var.get():
            messagebox.showwarning("CGU", "Vous devez accepter les conditions générales.")
            return
        
        key = self.key_entry.get()
        success, lic_type = config.activate_software(key)
        if success:
            msg = "Logiciel activé (Accès Illimité)." if lic_type == "STANDARD" else "Logiciel activé (Essai 14 Jours)."
            messagebox.showinfo("Succès", msg)
            self.start_animation_transition()
        else:
            messagebox.showerror("Erreur", "Clé d'activation invalide.")

    def start_animation_transition(self):
        self.clear_right()
        self.right_frame.configure(fg_color="#1a1a1a")
        c = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        c.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(c, text="MEDILINK OS", font=("SF Pro Display", 30, "bold"), text_color="#3498db").pack(pady=(0, 10))
        self.status_lbl = ctk.CTkLabel(c, text=tr("Initialisation..."), font=("Courier", 14), text_color="gray")
        self.status_lbl.pack(pady=5)
        self.progress = ctk.CTkProgressBar(c, width=300, height=10, progress_color="#2ecc71")
        self.progress.set(0)
        self.progress.pack(pady=20)
        
        self.anim_steps = [
            (0.1, tr("Vérification de l'intégrité système...")),
            (0.3, tr("Chiffrement du coffre-fort local (AES-256)...")),
            (0.5, tr("Génération des certificats de sécurité...")),
            (0.7, tr("Configuration de la base de données SQL...")),
            (0.9, tr("Démarrage des services hospitaliers...")),
            (1.0, tr("Configuration terminée."))
        ]
        self.run_animation_step(0)

    def run_animation_step(self, index):
        if index < len(self.anim_steps):
            val, text = self.anim_steps[index]
            self.progress.set(val)
            self.status_lbl.configure(text=text)
            self.after(800, lambda: self.run_animation_step(index + 1))
        else:
            self.after(500, self.finish_activation)

    def finish_activation(self):
        self.right_frame.configure(fg_color=("gray98", "#1a1a1a"))
        if db.is_first_run(): self.show_first_run_setup()
        else: self.show_login()

    def show_first_run_setup(self):
        self.clear_right()
        c = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        c.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        
        ctk.CTkLabel(c, text=tr("Configuration Initiale"), font=("Arial", 24, "bold")).pack(pady=20)
        
        ctk.CTkLabel(c, text=tr("Compte Administrateur (Médecin)"), font=("Arial", 16, "bold"), text_color="#3498db").pack(anchor="w", padx=20, pady=(10,5))
        self.name_e = ctk.CTkEntry(c, placeholder_text=tr("Nom Complet (ex: Dr. Martin)"), width=350); self.name_e.pack(pady=5)
        self.user_e = ctk.CTkEntry(c, placeholder_text=tr("Identifiant Connexion"), width=350); self.user_e.pack(pady=5)
        self.pass_e = ctk.CTkEntry(c, placeholder_text=tr("Mot de Passe Fort"), show="*", width=350); self.pass_e.pack(pady=5)
        
        ctk.CTkLabel(c, text=tr("Informations Officielles (Pour Ordonnances)"), font=("Arial", 16, "bold"), text_color="#3498db").pack(anchor="w", padx=20, pady=(20,5))
        self.rpps_e = ctk.CTkEntry(c, placeholder_text=tr("Numéro RPPS (11 chiffres)"), width=350); self.rpps_e.pack(pady=5)
        self.hosp_e = ctk.CTkEntry(c, placeholder_text=tr("Nom Cabinet / Hôpital"), width=350); self.hosp_e.pack(pady=5)
        self.addr_e = ctk.CTkEntry(c, placeholder_text=tr("Adresse Complète"), width=350); self.addr_e.pack(pady=5)
        self.phone_e = ctk.CTkEntry(c, placeholder_text=tr("Téléphone Pro"), width=350); self.phone_e.pack(pady=5)
        
        ctk.CTkButton(c, text=tr("Finaliser Installation"), width=350, height=45, command=self.do_setup, fg_color="#27ae60").pack(pady=30)

    def do_setup(self):
        try:
            if not all([self.name_e.get(), self.user_e.get(), self.pass_e.get(), self.rpps_e.get(), self.hosp_e.get()]):
                messagebox.showwarning("Incomplet", "Tous les champs sont obligatoires.")
                return

            success, recovery_key = db.create_user(self.user_e.get(), self.pass_e.get(), "admin", self.name_e.get())
            if success:
                db.update_user_details(self.user_e.get(), self.rpps_e.get(), self.hosp_e.get(), self.addr_e.get(), self.phone_e.get())
                self.show_recovery_key_dialog(recovery_key, True)
            else: messagebox.showerror("Erreur", "Erreur création utilisateur.")
        except ValueError as e: messagebox.showerror("Sécurité", str(e))

    def show_recovery_key_dialog(self, key, is_setup=False):
        d = ctk.CTkToplevel(self)
        d.title("CLÉ DE SÉCURITÉ")
        d.geometry("500x350")
        d.attributes("-topmost", True)
        
        ctk.CTkLabel(d, text=tr("⚠️ SAUVEGARDE OBLIGATOIRE"), font=("Arial", 20, "bold"), text_color="#e74c3c").pack(pady=20)
        ctk.CTkLabel(d, text="Voici votre Clé de Récupération unique.\nC'est le SEUL moyen de restaurer votre accès.", font=("Arial", 12)).pack(pady=10)
        
        k_entry = ctk.CTkEntry(d, width=350, font=("Courier", 16, "bold"), justify="center")
        k_entry.insert(0, key)
        k_entry.configure(state="readonly")
        k_entry.pack(pady=15)
        
        ctk.CTkButton(d, text=tr("Copier la clé"), command=lambda: self.clipboard_clear() or self.clipboard_append(key)).pack(pady=5)
        
        def close():
            d.destroy()
            if is_setup: self.show_login()
            
        ctk.CTkButton(d, text=tr("J'ai bien noté cette clé"), fg_color="#27ae60", command=close).pack(pady=20)

    def show_login(self):
        self.clear_right()
        c = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        c.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(c, text=tr("Connexion Sécurisée"), font=("Arial", 24, "bold")).pack(pady=30)
        self.u_entry = ctk.CTkEntry(c, placeholder_text=tr("Identifiant"), width=280, height=45)
        self.u_entry.pack(pady=10)
        self.p_entry = ctk.CTkEntry(c, placeholder_text=tr("Mot de passe"), show="*", width=280, height=45)
        self.p_entry.pack(pady=10)
        self.p_entry.bind("<Return>", lambda e: self.animate_login())
        
        self.login_btn = ctk.CTkButton(c, text=tr("Entrer"), width=280, height=45, fg_color="#2980b9", command=self.animate_login)
        self.login_btn.pack(pady=15)
        
        forgot_lbl = ctk.CTkLabel(c, text=tr("Mot de passe oublié ?"), font=("Arial", 11, "underline"), text_color="gray", cursor="hand2")
        forgot_lbl.pack(pady=5)
        forgot_lbl.bind("<Button-1>", lambda e: self.show_forgot_password())

    def show_forgot_password(self):
        self.clear_right()
        c = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        c.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(c, text=tr("Récupération d'Accès"), font=("Arial", 22, "bold")).pack(pady=20)
        
        ctk.CTkLabel(c, text=tr("Identifiant :"), anchor="w").pack(fill="x", padx=40)
        u_entry = ctk.CTkEntry(c, width=280)
        u_entry.pack(pady=5)
        
        ctk.CTkLabel(c, text=tr("Clé de Récupération (REC-...) :"), anchor="w").pack(fill="x", padx=40)
        k_entry = ctk.CTkEntry(c, width=280)
        k_entry.pack(pady=5)
        
        ctk.CTkLabel(c, text=tr("Nouveau Mot de Passe :"), anchor="w").pack(fill="x", padx=40)
        new_p_entry = ctk.CTkEntry(c, width=280, show="*")
        new_p_entry.pack(pady=5)
        
        def try_reset():
            user = u_entry.get()
            key = k_entry.get().strip()
            new_pass = new_p_entry.get()
            if db.verify_recovery_key(user, key):
                try:
                    db.reset_password(user, new_pass)
                    messagebox.showinfo("Succès", "Mot de passe réinitialisé.")
                    self.show_login()
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))
            else:
                messagebox.showerror("Erreur", "Identifiant ou Clé incorrecte.")

        ctk.CTkButton(c, text=tr("Réinitialiser"), width=280, fg_color="#e67e22", command=try_reset).pack(pady=20)
        ctk.CTkButton(c, text=tr("Annuler"), width=280, fg_color="gray", command=self.show_login).pack(pady=5)

    def animate_login(self):
        u_val = self.u_entry.get()
        p_val = self.p_entry.get()
        u = db.get_user(u_val)
        if u and sec_manager.check_password(p_val, u[2]):
            self.login_btn.configure(state="disabled", text="...")
            overlay = ctk.CTkFrame(self.right_frame, fg_color=("gray95", "#202020"))
            overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
            loader_lbl = ctk.CTkLabel(overlay, text=tr("Connexion Sécurisée").upper(), font=("Arial", 16, "bold"))
            loader_lbl.place(relx=0.5, rely=0.4, anchor="center")
            spinner = ctk.CTkProgressBar(overlay, width=200, height=6, mode="indeterminate")
            spinner.place(relx=0.5, rely=0.5, anchor="center")
            spinner.start()
            def finish(): self.perform_login(u)
            self.after(1000, finish)
        else:
            messagebox.showerror("Refusé", "Identifiants invalides.")

    def perform_login(self, u):
        self.logged_in_user = u
        LoginWindow.relaunch_needed = True
        db.log_activity(u[0], "Connexion session")
        db.log_audit(u[0], "LOGIN", "Connexion utilisateur réussie")
        self.destroy()

# --- MAIN APP ---
class MainApp(ctk.CTk):
    relaunch_login = False 
    def __init__(self, user): 
        super().__init__()
        self.user = user
        _, lic_msg = config.check_license_status()
        self.title(f"MedilinkOS - {user[4]} [{lic_msg}]")
        self.geometry("1400x900")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.timeout_id = None
        self.current_plan_date = datetime.now()
        self.privacy_mode = False
        self.privacy_overlay = None
        
        self.top_bar = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=("white", "#2b2b2b"))
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(self.top_bar, text="Medilink", font=("SF Pro Display", 22, "bold"), text_color="#3498db").pack(side="left", padx=20)
        ctk.CTkLabel(self.top_bar, text="|  Hospital Core", font=("Arial", 16), text_color="gray").pack(side="left")
        
        ctk.CTkButton(self.top_bar, text=tr("👁️‍🗨️ Mode Discret"), width=120, fg_color="#2c3e50", hover_color="#34495e", command=self.toggle_privacy_mode).pack(side="right", padx=10)
        
        self.clock_lbl = ctk.CTkLabel(self.top_bar, text="", font=("Arial", 14), text_color="gray")
        self.clock_lbl.pack(side="right", padx=20)
        self.update_clock()
        ctk.CTkButton(self.top_bar, text=tr("Déconnexion"), width=120, height=32, fg_color="#e74c3c", hover_color="#c0392b", command=lambda: self.logout(relaunch=True)).pack(side="right", padx=10)
        
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=("#f8f9fa", "#1e1e1e"))
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="NAVIGATION", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(20,10))
        self.add_nav(tr("Tableau de bord"), "dashboard", "📊")
        self.add_nav(tr("Tâches (To-Do)"), "tasks", "✅")
        self.add_nav(tr("Planning (GAP)"), "planning", "📅")
        self.add_nav(tr("Dossiers Patients"), "patients", "📂")
        self.add_nav(tr("Outils Médicaux"), "tools", "🧮")
        self.msg_btn = self.add_nav(tr("Messagerie"), "messaging", "💬")
        self.add_nav(tr("RDV, Facturation et IA"), "billing", "💳")
        if self.user[3] == "admin": 
            ctk.CTkLabel(self.sidebar, text=tr("SYSTÈME"), font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(20,10))
            self.add_nav(tr("Administration"), "admin", "⚙️")
        ctk.CTkLabel(self.sidebar, text=SIGNATURE, font=("Arial", 10), text_color="gray").pack(side="bottom", pady=20)

        self.main_view = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray92", "#121212"))
        self.main_view.grid(row=1, column=1, sticky="nsew")
        self.show_frame("dashboard")
        
        self.bind_all("<Any-KeyPress>", self.reset_timer)
        self.bind_all("<Any-Button>", self.reset_timer)
        self.reset_timer()
        self.check_notifications()

    def toggle_privacy_mode(self):
        if self.privacy_mode:
            if self.privacy_overlay: self.privacy_overlay.destroy()
            self.privacy_mode = False
        else:
            self.privacy_mode = True
            self.privacy_overlay = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
            self.privacy_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
            container = ctk.CTkFrame(self.privacy_overlay, fg_color="transparent")
            container.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(container, text="🔒", font=("Arial", 80)).pack(pady=20)
            ctk.CTkLabel(container, text="MODE CONFIDENTIALITÉ ACTIVÉ", font=("Arial", 24, "bold"), text_color="white").pack()
            btn = ctk.CTkButton(self.privacy_overlay, text="", fg_color="transparent", width=3000, height=3000, hover_color="#111", command=self.toggle_privacy_mode)
            btn.place(relx=0.5, rely=0.5, anchor="center")

    def reset_timer(self, event=None):
        if self.timeout_id: self.after_cancel(self.timeout_id)
        self.timeout_id = self.after(AUTO_LOGOUT_TIME_MS, self.auto_logout)

    def auto_logout(self):
        self.logout(relaunch=True)

    def check_notifications(self):
        try:
            count = db.get_unread_count(self.user[0])
            if count > 0: self.msg_btn.configure(text=f"💬 {tr('Messagerie')} ({count})", fg_color="#e74c3c", text_color="white")
            else: self.msg_btn.configure(text=f"💬 {tr('Messagerie')}", fg_color="transparent", text_color=("black", "white"))
            self.after(3000, self.check_notifications)
        except: pass

    def update_clock(self):
        self.clock_lbl.configure(text=datetime.now().strftime("%d/%m/%Y  •  %H:%M:%S"))
        self.after(1000, self.update_clock)

    def add_nav(self, text, cmd, icon):
        btn = ctk.CTkButton(self.sidebar, text=f"{icon}  {text}", anchor="w", fg_color="transparent", text_color=("black", "white"), hover_color=("gray85", "gray25"), height=45, corner_radius=8, command=lambda: self.show_frame(cmd))
        btn.pack(fill="x", padx=15, pady=2)
        return btn

    def show_frame(self, name):
        for w in self.main_view.winfo_children(): w.destroy()
        if name == "dashboard": self.render_dashboard()
        elif name == "tasks": self.render_tasks() 
        elif name == "planning": self.render_planning()
        elif name == "patients": self.render_patients()
        elif name == "tools": self.render_tools() 
        elif name == "messaging": self.render_messaging()
        elif name == "billing": self.render_billing()
        elif name == "admin": self.render_admin()

    def logout(self, relaunch=False):
        db.log_activity(self.user[0], "Déconnexion")
        MainApp.relaunch_login = relaunch
        self.destroy()

    def render_dashboard(self):
        greeting = "Hello" if config.config_data.get("language") == "EN" else "Bonjour"
        ctk.CTkLabel(self.main_view, text=f"{greeting}, {self.user[4]}", font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=30, pady=30)
        grid = ctk.CTkFrame(self.main_view, fg_color="transparent")
        grid.pack(fill="x", padx=30)
        def card(parent, title, val, color):
            c = MacCard(parent, width=220, height=130)
            c.pack(side="left", padx=(0, 20))
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=str(val), font=("Arial", 42, "bold"), text_color=color).pack(pady=(15,0))
            ctk.CTkLabel(c, text=title, font=("Arial", 14), text_color="gray").pack()
        apps = db.get_appointments(self.user[0])
        todays_rdv = [a for a in apps if a['date'].startswith(datetime.now().strftime("%Y-%m-%d"))]
        pending_tasks = len([t for t in db.get_tasks(self.user[0]) if t[2] == 0])
        
        card(grid, tr("Mes Tâches"), pending_tasks, "#9b59b6")
        card(grid, tr("RDV Aujourd'hui"), len(todays_rdv), "#e67e22")
        card(grid, tr("Messages non lus"), db.get_unread_count(self.user[0]), "#e74c3c")
        
        ctk.CTkButton(self.main_view, text=tr("🏥 Voir Plan du Service (Lits)"), font=("Arial", 16, "bold"), height=50, fg_color="#16a085", command=self.show_bed_map).pack(pady=20, padx=30, fill="x")

        ctk.CTkLabel(self.main_view, text=tr("Flux d'activité"), font=("SF Pro Display", 20, "bold")).pack(anchor="w", padx=30, pady=(10,10))
        act_f = MacCard(self.main_view)
        act_f.pack(fill="both", expand=True, padx=30, pady=(0,30))
        scroll = ctk.CTkScrollableFrame(act_f, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        for a, t, u in db.get_recent_activities(15):
            r = ctk.CTkFrame(scroll, fg_color="transparent")
            r.pack(fill="x", pady=5)
            ctk.CTkLabel(r, text=t[11:16], width=60, text_color="gray").pack(side="left")
            ctk.CTkLabel(r, text=f"• {u} : {a}", anchor="w").pack(side="left", fill="x")

    def show_bed_map(self):
        t = ctk.CTkToplevel(self)
        t.title(tr("Plan d'Occupation des Lits"))
        t.geometry("1000x700")
        scroll = ctk.CTkScrollableFrame(t)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        patients = db.get_patients()
        rooms_layout = {}
        for p in patients:
            room = p.get('h_chambre', '')
            if room and room != "?" and room.strip():
                rooms_layout[room] = f"{p['nom']} {p['prenom']}"
        row, col = 0, 0
        for i in range(101, 121):
            r_num = str(i)
            is_occupied = r_num in rooms_layout
            color = "#e74c3c" if is_occupied else "#2ecc71"
            txt = f"{tr('Chambre')} {r_num}\n" + (rooms_layout[r_num] if is_occupied else tr("LIBRE"))
            f = ctk.CTkFrame(scroll, fg_color=color, width=200, height=120)
            f.grid(row=row, column=col, padx=10, pady=10)
            f.pack_propagate(False)
            ctk.CTkLabel(f, text=txt, text_color="white", font=("Arial", 14, "bold")).pack(expand=True)
            col += 1
            if col > 3: col=0; row+=1

    def render_tasks(self):
        ctk.CTkLabel(self.main_view, text=tr("Mes Tâches"), font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=30, pady=30)
        input_f = MacCard(self.main_view)
        input_f.pack(fill="x", padx=30)
        
        self.task_entry = ctk.CTkEntry(input_f, placeholder_text=tr("Nouvelle tâche à faire..."), height=40)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=20, pady=20)
        self.task_entry.bind("<Return>", lambda e: self.add_task_action())
        
        ctk.CTkButton(input_f, text=tr("+ Ajouter"), width=100, height=40, command=self.add_task_action).pack(side="right", padx=20)
        
        self.tasks_scroll = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent")
        self.tasks_scroll.pack(fill="both", expand=True, padx=30, pady=20)
        self.refresh_tasks()

    def add_task_action(self):
        txt = self.task_entry.get()
        if txt:
            db.add_task(self.user[0], txt)
            self.task_entry.delete(0, END)
            self.refresh_tasks()

    def refresh_tasks(self):
        for w in self.tasks_scroll.winfo_children(): w.destroy()
        tasks = db.get_tasks(self.user[0])
        if not tasks:
            ctk.CTkLabel(self.tasks_scroll, text=tr("Aucune tâche en cours."), text_color="gray").pack(pady=20)
            return
            
        for t in tasks:
            is_done = t[2] == 1
            color = ("gray85", "gray25") if is_done else ("white", "#333")
            txt_color = "gray" if is_done else ("black", "white")
            f = MacCard(self.tasks_scroll, fg_color=color, height=50)
            f.pack(fill="x", pady=5)
            check_var = ctk.BooleanVar(value=is_done)
            chk = ctk.CTkCheckBox(f, text="", variable=check_var, width=30, command=lambda tid=t[0], v=check_var: self.toggle_task(tid, v))
            chk.pack(side="left", padx=15)
            ctk.CTkLabel(f, text=t[1], text_color=txt_color, font=("Arial", 14)).pack(side="left", padx=5)
            ctk.CTkButton(f, text="🗑️", width=40, fg_color="transparent", hover_color="#e74c3c", text_color=("black", "white"), command=lambda tid=t[0]: self.delete_task(tid)).pack(side="right", padx=10)

    def toggle_task(self, tid, var):
        status = 1 if var.get() else 0
        db.update_task_status(tid, status)
        self.refresh_tasks()

    def delete_task(self, tid):
        db.delete_task(tid)
        self.refresh_tasks()

    def render_tools(self):
        ctk.CTkLabel(self.main_view, text=tr("Outils Médicaux"), font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=30, pady=30)
        tabs = ctk.CTkTabview(self.main_view)
        tabs.pack(fill="both", expand=True, padx=30, pady=(0,30))
        self.setup_dfg_tool(tabs.add("DFG (Rein)"))
        self.setup_glasgow_tool(tabs.add("Score Glasgow"))

    def setup_dfg_tool(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(pady=20)
        ctk.CTkLabel(f, text=tr("Formule de Cockcroft-Gault"), font=("Arial", 16, "bold")).pack(pady=10)
        grid = ctk.CTkFrame(f, fg_color="transparent")
        grid.pack()
        ctk.CTkLabel(grid, text=tr("Âge (ans)")).grid(row=0, column=0, padx=10, pady=5)
        self.dfg_age = ctk.CTkEntry(grid, width=100); self.dfg_age.grid(row=0, column=1)
        ctk.CTkLabel(grid, text=tr("Poids (kg)")).grid(row=1, column=0, padx=10, pady=5)
        self.dfg_weight = ctk.CTkEntry(grid, width=100); self.dfg_weight.grid(row=1, column=1)
        ctk.CTkLabel(grid, text=tr("Créatinine (µmol/L)")).grid(row=2, column=0, padx=10, pady=5)
        self.dfg_creat = ctk.CTkEntry(grid, width=100); self.dfg_creat.grid(row=2, column=1)
        ctk.CTkLabel(grid, text=tr("Sexe")).grid(row=3, column=0, padx=10, pady=5)
        self.dfg_sex = ctk.CTkComboBox(grid, values=[tr("Homme"), tr("Femme")], width=100); self.dfg_sex.grid(row=3, column=1)
        ctk.CTkButton(f, text=tr("Calculer"), command=self.calc_dfg).pack(pady=20)
        self.dfg_res = ctk.CTkLabel(f, text="Result : - ml/min", font=("Arial", 18, "bold"), text_color="#3498db")
        self.dfg_res.pack()

    def calc_dfg(self):
        try:
            age = float(self.dfg_age.get())
            weight = float(self.dfg_weight.get())
            creat = float(self.dfg_creat.get())
            sex_factor = 1.04 if self.dfg_sex.get() in ["Femme", "Female"] else 1.23
            res = ((140 - age) * weight * sex_factor) / creat
            self.dfg_res.configure(text=f"Clairance : {res:.1f} ml/min")
        except: pass

    def setup_glasgow_tool(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(pady=20)
        ctk.CTkLabel(f, text=tr("Échelle de Coma de Glasgow"), font=("Arial", 16, "bold")).pack(pady=10)
        grid = ctk.CTkFrame(f, fg_color="transparent")
        grid.pack()
        ctk.CTkLabel(grid, text=tr("Ouverture des Yeux (Y)")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.gl_eye = ctk.CTkComboBox(grid, values=["4 - Spont", "3 - Voice", "2 - Pain", "1 - None"], width=200)
        self.gl_eye.grid(row=0, column=1)
        ctk.CTkLabel(grid, text=tr("Réponse Verbale (V)")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.gl_verb = ctk.CTkComboBox(grid, values=["5 - Orient", "4 - Confuse", "3 - Inapp", "2 - Incomp", "1 - None"], width=200)
        self.gl_verb.grid(row=1, column=1)
        ctk.CTkLabel(grid, text=tr("Réponse Motrice (M)")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.gl_mot = ctk.CTkComboBox(grid, values=["6 - Obey", "5 - Loc", "4 - Avoid", "3 - Flex", "2 - Ext", "1 - None"], width=200)
        self.gl_mot.grid(row=2, column=1)
        ctk.CTkButton(f, text=tr("Calculer"), command=self.calc_glasgow).pack(pady=20)
        self.gl_res = ctk.CTkLabel(f, text="Score : - / 15", font=("Arial", 18, "bold"), text_color="#3498db")
        self.gl_res.pack()

    def calc_glasgow(self):
        try:
            y = int(self.gl_eye.get().split(" ")[0])
            v = int(self.gl_verb.get().split(" ")[0])
            m = int(self.gl_mot.get().split(" ")[0])
            self.gl_res.configure(text=f"Score : {y+v+m} / 15")
        except: pass

    def render_planning(self):
        top = ctk.CTkFrame(self.main_view, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=30)
        ctk.CTkLabel(top, text=tr("Gestion des Rendez-vous"), font=("SF Pro Display", 28, "bold")).pack(side="left")
        date_ctrl = ctk.CTkFrame(top, fg_color="transparent")
        date_ctrl.pack(side="right")
        ctk.CTkButton(date_ctrl, text="<", width=40, command=lambda: self.change_plan_date(-1)).pack(side="left", padx=5)
        self.date_lbl = ctk.CTkLabel(date_ctrl, text=self.current_plan_date.strftime("%d/%m/%Y"), font=("Arial", 16, "bold"), width=120)
        self.date_lbl.pack(side="left", padx=5)
        ctk.CTkButton(date_ctrl, text=">", width=40, command=lambda: self.change_plan_date(1)).pack(side="left", padx=5)
        tools = MacCard(self.main_view, height=80)
        tools.pack(fill="x", padx=30, pady=(0, 20))
        grid = ctk.CTkFrame(tools, fg_color="transparent")
        grid.pack(pady=15)
        patients = [f"{p['id']}: {p['nom']} {p['prenom']}" for p in db.get_patients()]
        self.pat_combo = ctk.CTkComboBox(grid, values=patients, width=220)
        self.pat_combo.grid(row=0, column=0, padx=10)
        if patients: self.pat_combo.set(patients[0])
        self.time_e = ctk.CTkEntry(grid, placeholder_text="HH:MM", width=80); self.time_e.grid(row=0, column=1, padx=10); self.time_e.insert(0, "09:00")
        self.dur_e = ctk.CTkEntry(grid, placeholder_text="Min", width=60); self.dur_e.grid(row=0, column=2, padx=10); self.dur_e.insert(0, "15")
        self.room_e = ctk.CTkEntry(grid, placeholder_text=tr("Chambre"), width=100); self.room_e.grid(row=0, column=3, padx=10)
        self.purp_e = ctk.CTkEntry(grid, placeholder_text="Motif", width=250); self.purp_e.grid(row=0, column=4, padx=10)
        ctk.CTkButton(grid, text=tr("+ Planifier"), fg_color="#27ae60", command=self.add_app_action).grid(row=0, column=5, padx=10)
        self.app_scroll = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent")
        self.app_scroll.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_planning()

    def change_plan_date(self, days):
        self.current_plan_date += timedelta(days=days)
        self.date_lbl.configure(text=self.current_plan_date.strftime("%d/%m/%Y"))
        self.refresh_planning()

    def add_app_action(self):
        try:
            if not self.pat_combo.get(): return
            pid = int(self.pat_combo.get().split(":")[0])
            date_str = self.current_plan_date.strftime("%Y-%m-%d") + " " + self.time_e.get()
            db.add_appointment(pid, self.user[0], date_str, self.purp_e.get(), self.dur_e.get(), self.room_e.get())
            self.refresh_planning()
        except Exception as e: pass

    def refresh_planning(self):
        for w in self.app_scroll.winfo_children(): w.destroy()
        target_date = self.current_plan_date.strftime("%Y-%m-%d")
        is_staff = self.user[3] in ["admin", "secretaire"]
        apps = db.get_appointments(None if is_staff else self.user[0], date_filter=target_date)
        if not apps:
            ctk.CTkLabel(self.app_scroll, text=tr("Aucun rendez-vous."), text_color="gray").pack(pady=40)
            return
        for app in apps:
            c = MacCard(self.app_scroll, height=65)
            c.pack(fill="x", pady=5)
            sc = "#3498db"
            if app['status'] == "Réalisé": sc = "#2ecc71"
            elif app['status'] == "Annulé": sc = "gray"
            ctk.CTkLabel(c, text="⬤", text_color=sc, font=("Arial", 16)).pack(side="left", padx=(15,5))
            ctk.CTkLabel(c, text=app['date'][11:16], font=("Arial", 18, "bold"), text_color=sc).pack(side="left", padx=5)
            ctk.CTkLabel(c, text=f"{app['duration']} min | {app['room']}", font=("Arial", 11), text_color="gray").pack(side="left", padx=15)
            ctk.CTkLabel(c, text=app['patient'], font=("Arial", 16, "bold")).pack(side="left", padx=10)
            ctk.CTkLabel(c, text=f"{app['purpose']}", text_color="gray").pack(side="left", padx=10)
            act = ctk.CTkFrame(c, fg_color="transparent")
            act.pack(side="right", padx=15)
            ctk.CTkOptionMenu(act, values=["Prévu", "En Salle", "En Consultation", "Réalisé", "Annulé"], width=140, command=lambda s, aid=app['id']: self.update_app_status(aid, s)).pack(side="left", padx=5)
            ctk.CTkButton(act, text="Dossier", width=70, fg_color="transparent", border_width=1, text_color=("black", "white"), command=lambda pid=app['pid']: PatientEditor(self, pid)).pack(side="left", padx=5)

    def update_app_status(self, aid, status):
        db.update_appointment_status(aid, status)
        self.refresh_planning()

    def render_messaging(self):
        ctk.CTkLabel(self.main_view, text=tr("Messagerie Hospitalière"), font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=30, pady=30)
        container = ctk.CTkFrame(self.main_view, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=(0,30))
        user_list = ctk.CTkScrollableFrame(container, width=240, corner_radius=10)
        user_list.pack(side="left", fill="y", padx=(0, 15))
        self.chat_area = ctk.CTkFrame(container, corner_radius=10, fg_color=("white", "#2b2b2b"))
        self.chat_area.pack(side="left", fill="both", expand=True)
        self.selected_chat_user = None
        self.msg_scroll = ctk.CTkScrollableFrame(self.chat_area, fg_color="transparent")
        self.msg_scroll.pack(fill="both", expand=True, padx=15, pady=15)
        input_area = ctk.CTkFrame(self.chat_area, height=60, fg_color="transparent")
        input_area.pack(fill="x", padx=15, pady=15)
        self.msg_entry = ctk.CTkEntry(input_area, placeholder_text=tr("Message..."), height=40)
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.msg_entry.bind("<Return>", lambda e: self.send_msg())
        self.urgent_var = ctk.BooleanVar()
        ctk.CTkCheckBox(input_area, text="🚨 URGENT", variable=self.urgent_var, width=100, text_color="#e74c3c").pack(side="left", padx=5)
        ctk.CTkButton(input_area, text=tr("Envoyer"), width=90, height=40, command=self.send_msg).pack(side="right")
        for u in db.get_users():
            if u[0] != self.user[0]:
                ctk.CTkButton(user_list, text=f"{u[2]}\n{u[3]}", height=50, fg_color=("white", "#333"), text_color=("black", "white"), anchor="w", command=lambda uid=u[0], name=u[2]: self.load_chat(uid, name)).pack(fill="x", pady=2)

    def load_chat(self, uid, name):
        self.selected_chat_user = uid
        db.mark_messages_read(self.user[0], uid)
        self.refresh_chat()

    def refresh_chat(self):
        for w in self.msg_scroll.winfo_children(): w.destroy()
        if not self.selected_chat_user: return
        msgs = db.get_messages(self.user[0], self.selected_chat_user)
        for m in msgs:
            is_me = m[0] == self.user[0]
            is_urgent = m[4] == 1
            align = "e" if is_me else "w"
            bg_color = "#c0392b" if is_urgent else ("#3498db" if is_me else ("#ecf0f1", "#404040"))
            txt_color = "white" if is_urgent or is_me else ("black", "white")
            bubble = ctk.CTkFrame(self.msg_scroll, fg_color=bg_color, corner_radius=12)
            bubble.pack(anchor=align, pady=4, padx=10)
            content = m[1]
            if "[PATIENT:" in content:
                try:
                    pid = content.split("[PATIENT:")[1].split("]")[0]
                    display = content.split("] ")[1] if "] " in content else "Dossier"
                    ctk.CTkLabel(bubble, text="📂 PARTAGE", font=("Arial", 10, "bold"), text_color=txt_color).pack(padx=10, pady=(5,0))
                    ctk.CTkLabel(bubble, text=display, font=("Arial", 12), text_color=txt_color).pack(padx=10, pady=2)
                    ctk.CTkButton(bubble, text="Ouvrir", height=24, fg_color="white", text_color="black", command=lambda p=pid: PatientEditor(self, int(p))).pack(padx=10, pady=5)
                except: ctk.CTkLabel(bubble, text=content, text_color=txt_color).pack(padx=12, pady=8)
            else:
                prefix = "🚨 " if is_urgent else ""
                ctk.CTkLabel(bubble, text=prefix + content, text_color=txt_color, wraplength=350, justify="left").pack(padx=12, pady=8)
            status = " • Vu" if is_me and m[3] else ""
            ctk.CTkLabel(bubble, text=f"{m[2][11:16]}{status}", font=("Arial", 9), text_color=txt_color).pack(anchor="e", padx=10, pady=(0,4))

    def send_msg(self):
        if not self.selected_chat_user or not self.msg_entry.get(): return
        db.send_message(self.user[0], self.selected_chat_user, self.msg_entry.get(), 1 if self.urgent_var.get() else 0)
        self.msg_entry.delete(0, END); self.urgent_var.set(False); self.refresh_chat()

    def render_patients(self):
        header = ctk.CTkFrame(self.main_view, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=30)
        ctk.CTkLabel(header, text=tr("Dossiers Patients (DPI)"), font=("SF Pro Display", 28, "bold")).pack(side="left")
        ctk.CTkButton(header, text=tr("+ Admission"), command=lambda: PatientEditor(self, None)).pack(side="right")
        
        filter_f = ctk.CTkFrame(self.main_view, fg_color="transparent")
        filter_f.pack(fill="x", padx=30, pady=(0, 10))
        
        self.service_filter = ctk.CTkComboBox(filter_f, values=[tr("Tous les Services")] + SERVICES, width=200, command=self.filter_patients)
        self.service_filter.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(filter_f, placeholder_text=tr("🔍 Rechercher (Nom, IPP)..."), height=32)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_patients)
        
        self.pat_scroll = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent")
        self.pat_scroll.pack(fill="both", expand=True, padx=20)
        self.render_patient_list(db.get_patients())

    def filter_patients(self, event=None):
        query = self.search_entry.get().lower()
        service_sel = self.service_filter.get()
        all_p = db.get_patients()
        res = []
        for p in all_p:
            match_text = query in p['nom'].lower() or query in p['prenom'].lower() or query in p['ipp'].lower()
            match_service = service_sel == tr("Tous les Services") or p['service'] == service_sel
            if match_text and match_service:
                res.append(p)
        self.render_patient_list(res)

    def render_patient_list(self, patients):
        for w in self.pat_scroll.winfo_children(): w.destroy()
        if not patients:
            ctk.CTkLabel(self.pat_scroll, text=tr("Aucun patient trouvé."), text_color="gray").pack(pady=20)
            return
        for p in patients:
            c = MacCard(self.pat_scroll, height=70)
            c.pack(fill="x", pady=5)
            ctk.CTkLabel(c, text="👤", font=("Arial", 24)).pack(side="left", padx=20)
            info = ctk.CTkFrame(c, fg_color="transparent")
            info.pack(side="left", padx=10)
            ctk.CTkLabel(info, text=f"{p['nom']} {p['prenom']}", font=("Arial", 16, "bold")).pack(anchor="w")
            ctk.CTkLabel(info, text=f"IPP: {p['ipp']} | {p['service']}", text_color="gray").pack(anchor="w")
            ctk.CTkButton(c, text="Dossier", command=lambda pid=p['id']: PatientEditor(self, pid)).pack(side="right", padx=20)

    def render_billing(self):
        ctk.CTkLabel(self.main_view, text=tr("RDV, Facturation et IA"), font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=30, pady=30)
        card = MacCard(self.main_view)
        card.pack(fill="both", expand=True, padx=30, pady=10)
        ctk.CTkLabel(card, text=tr("Accès portail Web."), font=("Arial", 16), text_color="gray").pack(pady=40)
        ctk.CTkButton(card, text=tr("Ouvrir"), command=lambda: webbrowser.open("https://medilink-app.base44.app/")).pack(pady=20)

    def render_admin(self):
        ctk.CTkLabel(self.main_view, text=tr("Administration"), font=("SF Pro Display", 28, "bold")).pack(anchor="w", padx=30, pady=30)
        tab = ctk.CTkTabview(self.main_view)
        tab.pack(fill="both", expand=True, padx=20)
        self.setup_users_tab(tab.add(tr("Personnel")))
        self.setup_system_tab(tab.add(tr("Système")))

    def setup_users_tab(self, parent):
        h = ctk.CTkFrame(parent, fg_color="transparent")
        h.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(h, text=tr("+ Compte"), command=lambda: UserEditor(self)).pack(side="right")
        self.user_scroll = ctk.CTkScrollableFrame(parent)
        self.user_scroll.pack(fill="both", expand=True, padx=10)
        self.refresh_users()

    def refresh_users(self):
        for w in self.user_scroll.winfo_children(): w.destroy()
        for u in db.get_users():
            f = ctk.CTkFrame(self.user_scroll, height=50)
            f.pack(fill="x", pady=3)
            ctk.CTkLabel(f, text=f"{u[2]} [{u[3].upper()}]", font=("Arial", 14)).pack(side="left", padx=15)
            ctk.CTkButton(f, text="Edit", width=60, command=lambda uid=u[0]: UserEditor(self, uid)).pack(side="right", padx=10)
            if u[1] != "admin": ctk.CTkButton(f, text="X", width=40, fg_color="#e74c3c", command=lambda uid=u[0]: self.delete_u(uid)).pack(side="right")

    def delete_u(self, uid):
        if messagebox.askyesno("Sécurité", "Révoquer accès ?"): db.delete_user(uid); self.refresh_users()

    def setup_system_tab(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=20, pady=20)
        SectionTitle(f, tr("Interface")).pack(anchor="w", pady=(0, 10))
        self.theme_switch_admin = ctk.CTkSwitch(f, text=tr("Mode Sombre"), command=self.toggle_theme_admin)
        if ctk.get_appearance_mode() == "Dark": self.theme_switch_admin.select()
        self.theme_switch_admin.pack(anchor="w", pady=10)
        
        # --- i18n Select ---
        f_lang = ctk.CTkFrame(f, fg_color="transparent")
        f_lang.pack(anchor="w", pady=10)
        ctk.CTkLabel(f_lang, text=tr("Langue / Language")).pack(side="left", padx=(0,10))
        self.sys_lang_var = ctk.StringVar(value=config.config_data.get("language", "FR"))
        ctk.CTkOptionMenu(f_lang, values=["FR", "EN"], variable=self.sys_lang_var, command=self.sys_change_language).pack(side="left")

        SectionTitle(f, tr("Maintenance")).pack(anchor="w", pady=(20, 10))
        ctk.CTkLabel(f, text=f"Data: {config.data_root}").pack(anchor="w")
        ctk.CTkButton(f, text=tr("Sauvegarde ZIP"), command=self.do_backup).pack(pady=10, anchor="w")
        ctk.CTkButton(f, text=tr("Changer Dossier"), command=self.change_loc).pack(pady=10, anchor="w")

    def sys_change_language(self, choice):
        config.config_data["language"] = choice
        config.save_config()
        if messagebox.askyesno("Restart", "Redémarrer pour appliquer la langue ? / Restart to apply language changes?"):
            self.logout(relaunch=True)

    def toggle_theme_admin(self):
        if self.theme_switch_admin.get(): ctk.set_appearance_mode("Dark")
        else: ctk.set_appearance_mode("Light")

    def do_backup(self):
        ok, msg = config.create_backup()
        if ok: messagebox.showinfo("Backup", msg)
        else: messagebox.showerror("Err", msg)

    def change_loc(self):
        d = filedialog.askdirectory()
        if d and messagebox.askyesno("Attention", "Redémarrage requis."):
            config.set_data_path(d); self.logout(relaunch=True)

# --- USER EDITOR ---
class UserEditor(ctk.CTkToplevel):
    def __init__(self, parent, uid=None):
        super().__init__(parent)
        self.parent = parent
        self.uid = uid
        self.title(tr("Compte Utilisateur"))
        self.geometry("500x700")
        f = MacCard(self)
        f.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(f, text=tr("Compte Utilisateur"), font=("Arial", 14, "bold")).pack(pady=(10,5))
        self.n_e = ctk.CTkEntry(f, placeholder_text=tr("Nom Complet (ex: Dr. Martin)")); self.n_e.pack(pady=5, fill="x", padx=20)
        self.u_e = ctk.CTkEntry(f, placeholder_text=tr("Identifiant")); self.u_e.pack(pady=5, fill="x", padx=20)
        self.r_e = ctk.CTkComboBox(f, values=ROLES); self.r_e.pack(pady=5, fill="x", padx=20)
        self.p_e = ctk.CTkEntry(f, placeholder_text=tr("Mot de passe"), show="*"); self.p_e.pack(pady=5, fill="x", padx=20)
        
        ctk.CTkLabel(f, text=tr("Profil Médical (Ordonnances)"), font=("Arial", 14, "bold")).pack(pady=(20,5))
        self.rpps_e = ctk.CTkEntry(f, placeholder_text=tr("Numéro RPPS (11 chiffres)")); self.rpps_e.pack(pady=5, fill="x", padx=20)
        self.hosp_e = ctk.CTkEntry(f, placeholder_text=tr("Nom Cabinet / Hôpital")); self.hosp_e.pack(pady=5, fill="x", padx=20)
        self.addr_e = ctk.CTkEntry(f, placeholder_text=tr("Adresse Complète")); self.addr_e.pack(pady=5, fill="x", padx=20)
        self.phone_e = ctk.CTkEntry(f, placeholder_text=tr("Téléphone Pro")); self.phone_e.pack(pady=5, fill="x", padx=20)
        
        ctk.CTkButton(f, text=tr("Enregistrer"), command=self.save, fg_color="#27ae60").pack(pady=30)
        if uid: self.load()

    def load(self):
        u = db.get_user_by_id(self.uid)
        if u:
            self.n_e.insert(0, u[4])
            self.u_e.insert(0, u[1])
            self.r_e.set(u[3])
            if len(u) > 6 and u[6]: self.rpps_e.insert(0, u[6])
            if len(u) > 7 and u[7]: self.hosp_e.insert(0, u[7])
            if len(u) > 8 and u[8]: self.addr_e.insert(0, u[8])
            if len(u) > 9 and u[9]: self.phone_e.insert(0, u[9])

    def save(self):
        try:
            success, new_key = False, None
            if self.uid: 
                db.update_user(self.uid, self.u_e.get(), self.p_e.get(), self.r_e.get(), self.n_e.get(),
                               self.rpps_e.get(), self.hosp_e.get(), self.addr_e.get(), self.phone_e.get())
            else: 
                success, new_key = db.create_user(self.u_e.get(), self.p_e.get(), self.r_e.get(), self.n_e.get())
                if success:
                    db.update_user_details(self.u_e.get(), self.rpps_e.get(), self.hosp_e.get(), self.addr_e.get(), self.phone_e.get())
            
            self.parent.refresh_users()
            self.destroy()
            if success and new_key:
                messagebox.showinfo("Clé", f"CLÉ DE RÉCUPÉRATION :\n{new_key}")
        except Exception as e: messagebox.showerror("Err", str(e))

# --- PATIENT EDITOR ---
class PatientEditor(ctk.CTkToplevel):
    def __init__(self, parent, pid):
        super().__init__(parent)
        self.parent = parent
        self.pid = pid
        self.title(tr("Dossier Patient"))
        self.geometry("1400x900")
        top = ctk.CTkFrame(self, height=60, fg_color=("white", "#2b2b2b"))
        top.pack(fill="x")
        ctk.CTkLabel(top, text=tr("Dossier Patient"), font=("Arial", 20, "bold")).pack(side="left", padx=20)
        if self.pid: 
            ctk.CTkButton(top, text=tr("Droit Oubli (RGPD)"), fg_color="#c0392b", width=120, command=self.delete_patient).pack(side="right", padx=5)
            ctk.CTkButton(top, text="Export JSON", fg_color="#8e44ad", width=100, command=self.export_json).pack(side="right", padx=5)
            ctk.CTkButton(top, text=tr("Générer Lettre Sortie"), fg_color="#34495e", width=150, command=self.generate_discharge_letter).pack(side="right", padx=10)
            ctk.CTkButton(top, text=tr("Partager"), fg_color="#e67e22", width=100, command=self.share_patient).pack(side="right", padx=10)
        ctk.CTkButton(top, text="PDF", width=80, command=self.export_pdf).pack(side="right", padx=5)
        ctk.CTkButton(top, text=tr("Sauver"), fg_color="#2ecc71", width=100, command=self.save).pack(side="right", padx=10)
        self.tab = ctk.CTkTabview(self)
        self.tab.pack(fill="both", expand=True, padx=20)
        self.t_admin = self.tab.add("Admin")
        self.t_hosp = self.tab.add(tr("Hospitalisation"))
        self.t_nurse = self.tab.add(tr("Soins"))
        self.t_consult = self.tab.add(tr("Médical"))
        self.t_const = self.tab.add(tr("Constantes"))
        self.t_presc = self.tab.add(tr("Presc"))
        self.t_bio = self.tab.add(tr("Bio/Img"))
        self.fields = {}
        self.lists_data = {"presc": [], "obs": [], "nurse_notes": [], "constantes_history": []}
        self.setup_admin(); self.setup_hosp(); self.setup_nurse(); self.setup_consult(); self.setup_const(); self.setup_presc(); self.setup_bio()
        if pid: self.load()

    def get_current_doc_profile(self):
        u = db.get_user_by_id(self.parent.user[0])
        profile = {
            "name": u[4],
            "rpps": u[6] if len(u)>6 else "N/A",
            "hospital": u[7] if len(u)>7 else "Hôpital Medilink",
            "address": u[8] if len(u)>8 else "",
            "phone": u[9] if len(u)>9 else ""
        }
        return profile

    def add_f(self, p, lbl, key, width=200, vals=None, text_area=False):
        f = ctk.CTkFrame(p, fg_color="transparent")
        f.pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(f, text=lbl, text_color="gray", font=("Arial", 11)).pack(anchor="w")
        if text_area: e = ctk.CTkTextbox(f, width=width, height=80)
        elif vals: e = ctk.CTkComboBox(f, values=vals, width=width)
        else: e = ctk.CTkEntry(f, width=width)
        e.pack()
        self.fields[key] = e
        return e

    def share_patient(self):
        d = ctk.CTkToplevel(self); d.title("Partager"); d.geometry("300x400")
        s = ctk.CTkScrollableFrame(d); s.pack(fill="both", expand=True)
        for u in db.get_users():
            if u[0] != self.parent.user[0]: ctk.CTkButton(s, text=u[2], command=lambda uid=u[0]: self.do_share(uid, d)).pack(fill="x", pady=2)

    def do_share(self, target_uid, d):
        msg = f"Dossier partagé : [PATIENT:{self.pid}] {self.fields['nom'].get()} {self.fields['prenom'].get()}"
        db.send_message(self.parent.user[0], target_uid, msg)
        messagebox.showinfo("OK", "Envoyé"); d.destroy()

    def setup_admin(self):
        f = ctk.CTkFrame(self.t_admin, fg_color="transparent"); f.pack(fill="x", pady=10)
        self.add_f(f, tr("Nom"), "nom"); self.add_f(f, tr("Prénom"), "prenom")
        self.dob_entry = self.add_f(f, tr("DDN (JJ/MM/AAAA)"), "dob")
        self.dob_entry.bind("<KeyRelease>", self.format_dob)
        self.age_lbl = ctk.CTkLabel(f, text="Age: -", font=("Arial", 12, "bold"), text_color="#3498db")
        self.age_lbl.pack(side="left", padx=5)
        self.add_f(f, tr("Sexe"), "sexe", 100, [tr("Homme"), tr("Femme")])
        f2 = ctk.CTkFrame(self.t_admin, fg_color="transparent"); f2.pack(fill="x", pady=10)
        self.add_f(f2, "IPP", "ipp"); self.add_f(f2, tr("Mutuelle"), "mutuelle", 200, MUTUELLES)
        f3 = ctk.CTkFrame(self.t_admin, fg_color="transparent"); f3.pack(fill="x", pady=10)
        self.add_f(f3, tr("INS / NIR (Sécu)"), "ins", 200)
        self.consent_var = ctk.BooleanVar()
        ctk.CTkCheckBox(f3, text=tr("Consentement RGPD Signé"), variable=self.consent_var).pack(side="left", padx=20, pady=20)

    def format_dob(self, event):
        if event.keysym.lower() == "backspace": return
        val = self.dob_entry.get()
        if len(val) == 2 or len(val) == 5: self.dob_entry.insert(END, "/")
        elif len(val) > 10: self.dob_entry.delete(10, END); val = val[:10]
        if len(val) == 10:
            try:
                d = datetime.strptime(val, "%d/%m/%Y")
                age = (datetime.now() - d).days // 365
                self.age_lbl.configure(text=f"Age: {age} ans")
            except: self.age_lbl.configure(text="Date invalide")
        else: self.age_lbl.configure(text="Age: -")

    def setup_hosp(self):
        f = ctk.CTkFrame(self.t_hosp, fg_color="transparent"); f.pack(fill="x", pady=10)
        self.add_f(f, tr("Service"), "service", 200, SERVICES); self.add_f(f, tr("Chambre"), "h_chambre", 80); self.add_f(f, tr("Mode"), "h_mode", 150, MODES_ADMISSION)
        f2 = ctk.CTkFrame(self.t_hosp, fg_color="transparent"); f2.pack(fill="x", pady=10)
        self.add_f(f2, tr("Régime"), "h_regime", 150, REGIMES); self.add_f(f2, tr("Isolement"), "h_isolement", 150, ISOLEMENTS)
        self.add_f(self.t_hosp, tr("Motif Admission"), "h_motif", 800, text_area=True)

    def setup_nurse(self):
        f = ctk.CTkFrame(self.t_nurse, fg_color="transparent"); f.pack(fill="x", pady=10)
        self.add_f(f, tr("Chute"), "n_chute", 150, RISQUES); self.add_f(f, tr("Douleur"), "n_eva", 80)
        i = ctk.CTkFrame(self.t_nurse, fg_color="transparent"); i.pack(fill="x", padx=10)
        self.nurse_e = ctk.CTkEntry(i, placeholder_text=tr("Transmission..."), width=500); self.nurse_e.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(i, text=tr("+ Ajouter"), width=80, command=self.add_nurse).pack(side="left", padx=5)
        self.nurse_scroll = ctk.CTkScrollableFrame(self.t_nurse); self.nurse_scroll.pack(fill="both", expand=True, padx=10)

    def add_nurse(self, txt=None, dt=None):
        t = txt if txt else self.nurse_e.get()
        if not t: return
        d = dt if dt else datetime.now().strftime("%d/%m %H:%M")
        if not txt: self.lists_data["nurse_notes"].append({"date": d, "text": t}); self.nurse_e.delete(0, END)
        f = ctk.CTkFrame(self.nurse_scroll, fg_color=("white", "gray30")); f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=d, text_color="gray", width=100).pack(side="left"); ctk.CTkLabel(f, text=t).pack(side="left")

    def setup_consult(self):
        f = ctk.CTkFrame(self.t_consult, fg_color="transparent"); f.pack(fill="x", pady=10)
        self.add_f(f, tr("Antécédents"), "ant_med", 400, text_area=True); self.add_f(f, tr("Allergies"), "allergies", 400, text_area=True)
        cim_f = ctk.CTkFrame(self.t_consult, fg_color="transparent"); cim_f.pack(fill="x", padx=10)
        ctk.CTkLabel(cim_f, text=tr("Codage CIM-10 :")).pack(side="left")
        self.cim_combo = ctk.CTkComboBox(cim_f, values=list(CIM10_DATA.keys()), width=200); self.cim_combo.pack(side="left", padx=5)
        ctk.CTkButton(cim_f, text=tr("Ajouter Diagnostic"), width=120, command=self.add_cim10).pack(side="left")
        i = ctk.CTkFrame(self.t_consult, fg_color="transparent"); i.pack(fill="x", padx=10, pady=5)
        self.obs_e = ctk.CTkEntry(i, placeholder_text=tr("Observation..."), width=500); self.obs_e.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(i, text=tr("Ajouter Obs"), width=80, command=self.add_obs).pack(side="left", padx=5)
        self.obs_scroll = ctk.CTkScrollableFrame(self.t_consult); self.obs_scroll.pack(fill="both", expand=True, padx=10)

    def add_cim10(self):
        diag = self.cim_combo.get()
        code = CIM10_DATA.get(diag, "???")
        text = f"Diagnostic: {diag} (CIM-10: {code})"
        self.add_obs(text)

    def add_obs(self, txt=None, dt=None):
        t = txt if txt else self.obs_e.get()
        if not t: return
        d = dt if dt else datetime.now().strftime("%d/%m %H:%M")
        if not txt: self.lists_data["obs"].append({"date": d, "text": t}); self.obs_e.delete(0, END)
        f = ctk.CTkFrame(self.obs_scroll, fg_color=("white", "gray30")); f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=d, text_color="gray", width=100).pack(side="left"); ctk.CTkLabel(f, text=t).pack(side="left")

    def setup_const(self):
        i = ctk.CTkFrame(self.t_const, fg_color="transparent"); i.pack(fill="x", padx=10, pady=10)
        self.c_ta = ctk.CTkEntry(i, placeholder_text="TA", width=60); self.c_ta.pack(side="left", padx=5)
        self.c_fc = ctk.CTkEntry(i, placeholder_text="FC", width=60); self.c_fc.pack(side="left", padx=5)
        self.c_temp = ctk.CTkEntry(i, placeholder_text="T°", width=60); self.c_temp.pack(side="left", padx=5)
        ctk.CTkButton(i, text=tr("+ Ajouter"), command=self.add_constantes).pack(side="left", padx=10)
        self.const_scroll = ctk.CTkScrollableFrame(self.t_const); self.const_scroll.pack(fill="both", expand=True, padx=10)

    def add_constantes(self, data=None):
        d = data if data else {"date": datetime.now().strftime("%d/%m %H:%M"), "ta": self.c_ta.get(), "fc": self.c_fc.get(), "temp": self.c_temp.get()}
        if not data and not d["ta"]: return
        if not data: 
            self.lists_data["constantes_history"].insert(0, d)
            self.c_ta.delete(0, END); self.c_fc.delete(0, END); self.c_temp.delete(0, END)
        f = ctk.CTkFrame(self.const_scroll); f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=f"{d['date']} | TA: {d['ta']} | FC: {d['fc']} | T°: {d['temp']}").pack(side="left", padx=10)

    def setup_presc(self):
        top = ctk.CTkFrame(self.t_presc, fg_color="transparent"); top.pack(fill="x", padx=10, pady=10)
        self.drug_n = ctk.CTkEntry(top, placeholder_text=tr("Médicament"), width=200); self.drug_n.pack(side="left", padx=5)
        self.drug_d = ctk.CTkEntry(top, placeholder_text=tr("Dose"), width=80); self.drug_d.pack(side="left", padx=5)
        self.drug_f = ctk.CTkEntry(top, placeholder_text=tr("Posologie"), width=120); self.drug_f.pack(side="left", padx=5)
        ctk.CTkButton(top, text=tr("+ Ajouter"), command=self.add_presc).pack(side="left", padx=5)
        ctk.CTkButton(top, text=tr("Imprimer"), command=self.print_ordo).pack(side="right")
        self.presc_scroll = ctk.CTkScrollableFrame(self.t_presc); self.presc_scroll.pack(fill="both", expand=True, padx=10)

    def add_presc(self, data=None):
        d = data if data else {"name": self.drug_n.get(), "dose": self.drug_d.get(), "freq": self.drug_f.get()}
        if not d["name"]: return
        if not data: self.lists_data["presc"].append(d); self.drug_n.delete(0, END)
        f = ctk.CTkFrame(self.presc_scroll); f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=f"{d['name']} - {d['dose']} ({d['freq']})").pack(side="left", padx=10)

    def setup_bio(self):
        top = ctk.CTkFrame(self.t_bio, fg_color="transparent"); top.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(top, text=tr("Ajouter Doc"), command=self.add_doc).pack(side="left")
        self.doc_scroll = ctk.CTkScrollableFrame(self.t_bio); self.doc_scroll.pack(fill="both", expand=True, padx=10)

    def add_doc(self):
        if not self.pid: return
        path = filedialog.askopenfilename()
        if path:
            dest = os.path.join(config.img_folder, str(self.pid))
            if not os.path.exists(dest): os.makedirs(dest)
            shutil.copy(path, os.path.join(dest, os.path.basename(path)))
            db.add_image(self.pid, os.path.join(dest, os.path.basename(path)), "Doc")
            self.load_docs()

    def load_docs(self):
        for w in self.doc_scroll.winfo_children(): w.destroy()
        for i in db.get_images(self.pid):
            f = ctk.CTkFrame(self.doc_scroll); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=os.path.basename(i[2])).pack(side="left", padx=10)
            ctk.CTkButton(f, text=tr("Ouvrir"), width=50, command=lambda p=i[2]: open_file_windows(p)).pack(side="right", padx=5)

    def save(self):
        ident = {k: v.get() if isinstance(v, ctk.CTkEntry) or isinstance(v, ctk.CTkComboBox) else v.get("1.0", END).strip() for k, v in self.fields.items() if not k.startswith("c_")}
        med = {"constantes_history": self.lists_data["constantes_history"], "prescriptions": self.lists_data["presc"], "observations": self.lists_data["obs"], "nurse_notes": self.lists_data["nurse_notes"]}
        try:
            if not ident["ipp"]: raise ValueError("IPP Requis")
            self.pid = db.save_patient(
                self.parent.user[0], 
                self.pid, 
                ident["ipp"], 
                ident, 
                med, 
                ident["service"],
                ident["ins"],
                self.consent_var.get()
            )
            messagebox.showinfo("OK", "Sauvegardé / Saved"); self.parent.show_frame("patients")
        except Exception as e: messagebox.showerror("Err", str(e))

    def load(self):
        d = db.get_full_patient(self.pid, self.parent.user[0])
        if not d: return
        ident = d['identity']; med = d['medical']
        for k, v in self.fields.items():
            val = ident.get(k, "")
            if k == 'ipp': val = d['ipp']
            if k == 'ins': val = d['ins']
            if k == 'service': val = d['service']
            if isinstance(v, ctk.CTkComboBox): v.set(val)
            elif isinstance(v, ctk.CTkTextbox): v.delete("1.0", END); v.insert("1.0", val)
            else: v.delete(0, END); v.insert(0, val)
        self.consent_var.set(bool(d['consent']))
        if self.dob_entry.get(): self.format_dob(type('obj', (object,), {'keysym': ''}))
        self.lists_data["presc"] = med.get("prescriptions", [])
        for p in self.lists_data["presc"]: self.add_presc(p)
        self.lists_data["obs"] = med.get("observations", [])
        for o in self.lists_data["obs"]: self.add_obs(o["text"], o["date"])
        self.lists_data["nurse_notes"] = med.get("nurse_notes", [])
        for n in self.lists_data["nurse_notes"]: self.add_nurse(n["text"], n["date"])
        self.lists_data["constantes_history"] = med.get("constantes_history", [])
        for c in self.lists_data["constantes_history"]: self.add_constantes(c)
        self.load_docs()

    def delete_patient(self):
        if messagebox.askyesno("DANGER", "Suppression définitive (RGPD) ? / Delete permanently?"):
             db.delete_patient_securely(self.pid, self.parent.user[0])
             self.destroy()
             self.parent.show_frame("patients")
             messagebox.showinfo("Succès", "Données effacées / Data deleted.")

    def export_json(self):
        d = db.get_full_patient(self.pid, self.parent.user[0])
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f:
            with open(f, 'w') as outfile: json.dump(d, outfile, indent=4, default=str)
            messagebox.showinfo("Export", "Fichier JSON généré.")

    def generate_discharge_letter(self):
        ident = {k: self.fields[k].get() for k in ["nom", "prenom", "dob", "ipp", "service", "ins"]}
        motif = self.fields["h_motif"].get("1.0", END).strip()
        obs = "<br>".join([f"- {o['text']}" for o in self.lists_data['obs'][-5:]]) 
        traitement = "<br>".join([f"- {p['name']} {p['dose']} {p['freq']}" for p in self.lists_data['presc']])
        doc_profile = self.get_current_doc_profile()
        lieu = doc_profile['address'].split(',')[-1].strip() if ',' in doc_profile['address'] else "l'hôpital"
        
        html = f"""
        <h2>LETTRE DE SORTIE</h2>
        <div style="background:#f9f9f9; padding:15px; border-left:4px solid #2980b9; margin-bottom:20px;">
            <p><b>Patient :</b> {ident['nom']} {ident['prenom']}</p>
            <p><b>Né(e) le :</b> {ident['dob']} | <b>IPP :</b> {ident['ipp']}</p>
            <p><b>INS :</b> {ident['ins']} | <b>Service :</b> {ident['service']}</p>
        </div>
        <h3>Motif d'Hospitalisation</h3><p>{motif if motif else "Non renseigné"}</p>
        <h3>Résumé Clinique</h3><p>{obs if obs else "Aucune observation majeure consignée."}</p>
        <h3>Traitement de Sortie</h3><p>{traitement if traitement else "Aucun traitement particulier."}</p>
        <div class="signature-box">
            <p>Fait à {lieu}, le {datetime.now().strftime('%d/%m/%Y')}</p>
            <div class="signature-line"></div>
            <p><b>{doc_profile['name']}</b></p>
        </div>
        """
        generate_html_report(doc_profile, f"Sortie_{ident['nom']}", html, "sortie")

    def print_ordo(self):
        ident = {k: self.fields[k].get() for k in ["nom", "prenom", "dob", "sexe", "ins"]}
        doc_profile = self.get_current_doc_profile()
        med_rows = ""
        for p in self.lists_data["presc"]: med_rows += f"<div class='med-item'><div class='med-name'>{p['name']}</div><div>{p['dose']} - {p['freq']}</div></div>"
        
        html = f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px;">
            <div>
                <h3>{doc_profile['name']}</h3><p>{doc_profile['hospital']}</p>
                <p>RPPS: {doc_profile['rpps']}</p><p>{doc_profile['address']}</p><p>Tel: {doc_profile['phone']}</p>
            </div>
            <div style="text-align: right;"><p>Le {datetime.now().strftime('%d/%m/%Y')}</p></div>
        </div>
        <div style="margin-bottom: 30px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;">
            <p><b>Patient :</b> {ident['nom']} {ident['prenom']}</p>
            <p>Né(e) le : {ident['dob']} ({ident.get('sexe', '?')})</p>
            <p>INS : {ident.get('ins', 'Non renseigné')}</p>
        </div>
        <h2 style="text-align: center; text-decoration: underline; margin: 30px 0;">ORDONNANCE</h2>
        <div style="margin: 20px 10px; min-height: 400px;">
            {med_rows if med_rows else "<p>Aucune prescription enregistrée.</p>"}
        </div>
        <div class="signature-box">
            <p>Signature & Tampon :</p><div class="signature-line"></div><p>{doc_profile['name']}</p>
        </div>
        """
        generate_html_report(doc_profile, f"Ordonnance_{ident['nom']}", html, "ordo")

    def export_pdf(self):
        ident = {k: v.get() for k, v in self.fields.items() if isinstance(v, ctk.CTkEntry) or isinstance(v, ctk.CTkComboBox)}
        doc_profile = self.get_current_doc_profile()
        html = f"""<h2>Dossier Hospitalier: {ident['nom']} {ident['prenom']}</h2><table><tr><th>IPP</th><td>{ident['ipp']}</td><th>Service</th><td>{ident['service']}</td></tr></table><h3>Observations</h3><ul>{"".join([f"<li>{o['date']}: {o['text']}</li>" for o in self.lists_data['obs']])}</ul>"""
        generate_html_report(doc_profile, f"Dossier_{ident['nom']}", html)

if __name__ == "__main__":
    while LoginWindow.relaunch_needed:
        if not LoginWindow.relaunch_needed: break
        lw = LoginWindow() 
        lw.mainloop() 
        if LoginWindow.relaunch_needed and lw.logged_in_user:
            MainApp.relaunch_login = False 
            app = MainApp(user=lw.logged_in_user) 
            app.mainloop()
            LoginWindow.relaunch_needed = MainApp.relaunch_login
        else: break

# MEDILINKOS APP POWERED BY ENZO MAISONNIER - UPDATE 02-05-2026 #
