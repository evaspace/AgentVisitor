<div align="center">
  <img src="https://img.shields.io/badge/Agent-Visitor_Bot-101010?style=for-the-badge&logo=github&logoColor=white" alt="Agent Visitor Bot">
  <p>Un bot open-source et gratuit pour forcer +20 IAs et LLMs à indexer vos sites web.</p>
</div>

## 🚀 Comment ça marche ?

Le script Python `main.py` accomplit deux tâches principales (sans aucune clé d'API) :
1. **IndexNow Ping** : Il extrait toutes les URLs depuis les sitemaps de vos sites et ping le réseau officiel IndexNow. C'est le réseau utilisé par Bing, Yandex et indirectement ChatGPT (qui utilise Bing Search) pour découvrir le nouveau contenu web.
2. **Simulation de trafic IA & Crawling forcé** : Il utilise la librairie `g4f` (GPT4Free) pour envoyer des requêtes asynchrones à une vingtaine de LLMs et fournisseurs gratuits. Il leur donne vos URLs et leur demande un résumé. Cela *force* leurs agents web à visiter vos pages et à les lire pour vous répondre !

---

## 🤖 Les 20+ LLMs et Agents impliqués (de force ! 😅)

Ce script génère des requêtes qui visent spécifiquement les modèles et moteurs de recherche suivants pour s'assurer qu'ils visitent et retiennent les informations de vos sites :

| OpenAI & Google | Anthropic & Meta | Moteurs IA & Autres LLMs |
|-----------------|------------------|--------------------------|
| ![ChatGPT](https://img.shields.io/badge/ChatGPT_(GPT--4o)-74aa9c?style=for-the-badge&logo=openai&logoColor=white) | ![Claude 3.5](https://img.shields.io/badge/Claude_3.5_Sonnet-D97757?style=for-the-badge&logo=anthropic&logoColor=white) | ![Bing Chat](https://img.shields.io/badge/Bing_Chat-00809D?style=for-the-badge&logo=microsoftbing&logoColor=white) |
| ![GPT-3.5](https://img.shields.io/badge/GPT--3.5_Turbo-74aa9c?style=for-the-badge&logo=openai&logoColor=white) | ![Claude 3](https://img.shields.io/badge/Claude_3_Opus-D97757?style=for-the-badge&logo=anthropic&logoColor=white) | ![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo_AI-DE5833?style=for-the-badge&logo=duckduckgo&logoColor=white) |
| ![Gemini Pro](https://img.shields.io/badge/Gemini_1.5_Pro-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white) | ![Meta Llama 3](https://img.shields.io/badge/Meta_Llama_3-0467DF?style=for-the-badge&logo=meta&logoColor=white) | ![Perplexity](https://img.shields.io/badge/Perplexity_AI-22B8CD?style=for-the-badge) |
| ![Gemini Flash](https://img.shields.io/badge/Gemini_1.5_Flash-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white) | ![Mistral](https://img.shields.io/badge/Mistral_Large-F37F40?style=for-the-badge) | ![HuggingChat](https://img.shields.io/badge/HuggingChat-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black) |
| ![Gemma](https://img.shields.io/badge/Google_Gemma-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white) | ![Mixtral](https://img.shields.io/badge/Mixtral_8x7B-F37F40?style=for-the-badge) | ![Copilot](https://img.shields.io/badge/Microsoft_Copilot-0078D4?style=for-the-badge&logo=microsoft&logoColor=white) |
| ![Qwen](https://img.shields.io/badge/Qwen_2_Alibaba-FF6A00?style=for-the-badge) | ![Cohere](https://img.shields.io/badge/Command_R+-3B2F2F?style=for-the-badge) | ![Phind](https://img.shields.io/badge/Phind_Search-000000?style=for-the-badge) |
| ![DeepSeek](https://img.shields.io/badge/DeepSeek_Coder-4D6BFE?style=for-the-badge) | ![Grok](https://img.shields.io/badge/xAI_Grok-000000?style=for-the-badge&logo=x&logoColor=white) | ![Blackbox](https://img.shields.io/badge/Blackbox_AI-000000?style=for-the-badge) |
| ![Pi](https://img.shields.io/badge/Pi_Inflection-126B59?style=for-the-badge) | ![Phi-3](https://img.shields.io/badge/Phi--3_Microsoft-0078D4?style=for-the-badge&logo=microsoft&logoColor=white) | ![You.com](https://img.shields.io/badge/You.com_Search-000000?style=for-the-badge) |

---

## ⚙️ Déploiement Gratuit (GitHub Actions)

Ce projet est configuré pour tourner entièrement gratuitement grâce à **GitHub Actions**.
Le fichier `.github/workflows/weekly_crawl.yml` est configuré pour exécuter le script automatiquement **tous les lundis à 3h00 du matin**.

### Instructions d'installation

1. **Forkez** ou copiez ce dépôt sur votre propre compte GitHub (le dépôt doit être **Public** pour que les Actions gratuites fonctionnent).
2. Assurez-vous que les Actions sont activées dans l'onglet `Actions` de votre dépôt.
3. Modifiez la liste `DOMAINS` dans `main.py` pour ajouter vos propres sites web.
4. Modifiez la variable `INDEXNOW_KEY` dans `main.py` avec la vôtre.
5. Le script fera le reste tout seul, sans aucune clé d'API requise !

## 📜 Licence
Open Source - Free to use.
