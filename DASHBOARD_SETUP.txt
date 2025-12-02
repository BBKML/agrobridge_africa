DASHBOARD & CMS - INSTRUCTIONS DE MISE EN PLACE
=======================

Le système de dashboard et CMS pour AgroBridge Africa est maintenant prêt.

ÉTAPES DE CONFIGURATION
=======================

1. APPLIQUER LES MIGRATIONS DE BD
-----------------------------------
Ouvrez PowerShell dans le répertoire du projet et lancez :

```powershell
python manage.py makemigrations website
python manage.py migrate
```

2. CRÉER UN UTILISATEUR ADMINISTRATEUR
--------------------------------------
```powershell
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte admin avec identifiants de votre choix.

3. LANCER LE SERVEUR DE DÉVELOPPEMENT
--------------------------------------
```powershell
python manage.py runserver
```

4. ACCÉDER AU DASHBOARD
-----------------------
- Admin Django classique : http://localhost:8000/admin/
- Dashboard personnalisé : http://localhost:8000/dashboard/ (nécessite connexion en tant que staff)

FONCTIONNALITÉS
===============

📊 DASHBOARD (http://localhost:8000/dashboard/)
   - Vue d'ensemble : nombre de messages, produits, services
   - Messages récents
   - Accès rapide aux sections à éditer

📝 GESTION DES CONTENUS (http://localhost:8000/dashboard/content/<section>/)
   Sections disponibles :
   - hero : Section Hero (titre, sous-titre, image)
   - features : Nos forces
   - products_intro : Introduction Produits
   - gallery : Galerie
   - cta : Appel à l'action
   - about : À propos
   - services_intro : Introduction Services

📦 GESTION DES PRODUITS
   - Lister tous les produits
   - Créer/éditer/supprimer
   - Upload d'images
   - Ordre d'affichage
   - Activation/désactivation

⚙️ GESTION DES SERVICES
   - Lister tous les services
   - Créer/éditer/supprimer
   - Icônes (emojis)
   - Ordre d'affichage
   - Activation/désactivation

💬 GESTION DES MESSAGES DE CONTACT
   - Voir tous les messages
   - Marquer comme lu/non lu
   - Filtrer (tous / non lus)
   - Supprimer les messages
   - Détail complet avec infos de contact

MODÈLES BD
===========

ContactMessage
   - name (CharField) : nom du visiteur
   - email (EmailField) : email
   - phone (CharField, optionnel) : téléphone
   - subject (CharField, optionnel) : sujet
   - message (TextField) : contenu du message
   - is_read (BooleanField) : si lu par l'admin
   - created_at (DateTimeField) : date d'envoi

PageContent
   - section (CharField, unique) : identifiant de section
   - title (CharField) : titre
   - subtitle (CharField, optionnel) : sous-titre
   - description (TextField, optionnel) : description
   - image (ImageField, optionnel) : image
   - updated_at / created_at : dates

Product
   - name (CharField) : nom du produit
   - name_en (CharField, optionnel) : nom anglais
   - description (TextField) : description
   - features (TextField) : caractéristiques (une par ligne)
   - image (ImageField) : image du produit
   - order (IntegerField) : ordre d'affichage
   - is_active (BooleanField) : actif ou non
   - updated_at / created_at : dates

Service
   - name (CharField) : nom du service
   - icon (CharField) : emoji ou symbole
   - description (TextField) : description
   - features (TextField) : caractéristiques (une par ligne)
   - order (IntegerField) : ordre d'affichage
   - is_active (BooleanField) : actif ou non
   - updated_at / created_at : dates

ADMIN DJANGO (/admin/)
======================
Les modèles sont enregistrés dans l'admin Django standard pour gestion avancée :
- Interface classique de Django
- Filtres, recherche, tri
- Édition en masse
- Permissions granulaires

SÉCURITÉ
========
- Seuls les utilisateurs avec is_staff=True peuvent accéder au dashboard
- Les données de contact sont protégées
- Les formulaires utilisent CSRF tokens
- Les fichiers uploadés sont validés

PROCHAINES ÉTAPES RECOMMANDÉES
===============================
1. Éditez les contenus et produits via le dashboard
2. Accédez à http://localhost:8000/contact/ pour tester le formulaire de contact
3. Consultez les messages dans le dashboard
4. Personnalisez les templates si nécessaire
5. Déployez en production en configurant les bonnes permissions

TROUBLESHOOTING
===============
- Erreur 403 Forbidden : Vérifiez que l'utilisateur est staff (is_staff=True)
- Images ne s'affichent pas : Vérifiez MEDIA_ROOT et MEDIA_URL dans settings.py
- Migrations échouées : Assurez-vous que la BD est accessible
- Messages ne s'enregistrent pas : Vérifiez que le formulaire de contact envoie bien les données

SUPPORT
=======
Pour toute question ou bug, consultez la documentation Django :
https://docs.djangoproject.com/
