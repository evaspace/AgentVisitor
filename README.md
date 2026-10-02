# Agent Visitor Bot

Ce projet est un bot open-source gratuit conçu pour forcer les agents IA (LLMs) et les moteurs de recherche à explorer et indexer une série de sites web de manière régulière.

## Comment ça marche ?

Le script Python `main.py` accomplit deux tâches principales :
1. **IndexNow Ping** : Il extrait toutes les URLs depuis les sitemaps des sites listés et ping le réseau IndexNow (utilisé par Bing, Yandex, et indirectement ChatGPT/GPTBot) pour les notifier des mises à jour.
2. **Simulation de trafic IA** : Il utilise la librairie `g4f` (GPT4Free) pour envoyer gratuitement des prompts à différents LLMs (qui ont accès à Internet) en leur demandant de lire et de résumer les pages du site. Cela déclenche le crawler web de l'IA et génère une vraie visite de la part d'un agent IA.

## Déploiement Gratuit (GitHub Actions)

Ce projet est configuré pour tourner entièrement gratuitement grâce à **GitHub Actions**.
Le fichier `.github/workflows/weekly_crawl.yml` est configuré pour exécuter le script automatiquement **tous les lundis à 3h00 du matin**.

### Instructions d'installation

1. **Forkez** ou copiez ce dépôt sur votre propre compte GitHub.
2. Assurez-vous que les Actions sont activées dans l'onglet `Actions` de votre dépôt.
3. Modifiez la liste `DOMAINS` dans `main.py` pour ajouter vos propres sites web.
4. Générez une clé [IndexNow](https://www.bing.com/indexnow) et placez-la à la racine de votre site (un fichier `votre-cle.txt` contenant `votre-cle`).
5. Modifiez la variable `INDEXNOW_KEY` dans `main.py` avec votre clé.
6. Le script fera le reste tout seul, sans aucune clé d'API requise !

## Licence
Open Source - Free to use.
