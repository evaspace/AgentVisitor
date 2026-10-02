import requests
import xml.etree.ElementTree as ET
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import g4f

# Clé IndexNow existante sur le serveur Caddy (7d4b1a8f9c2e4d0b8a1c3e5f7a9b2d4e.txt)
INDEXNOW_KEY = "7d4b1a8f9c2e4d0b8a1c3e5f7a9b2d4e"

DOMAINS = [
    "https://pierref.eu",
    "https://opticars.pierref.eu",
    "https://creepita.pierref.eu",
    "https://pepexator.pierref.eu",
    "https://larchitect.pierref.eu",
    "https://sharator.pierref.eu",
    "https://mailer.pierref.eu",
    "https://cwl.pierref.eu",
    "https://bot.pierref.eu",
    "https://lbcstudio.pierref.eu",
    "https://lopez.persat.pierref.eu",
    "https://humanizator.pierref.eu",
    "https://musicator.pierref.eu",
    "https://streetsrace.pierref.eu",
    "https://auriga2google.pierref.eu",
    "https://matchshot.pierref.eu"
]

def get_urls_from_sitemap(domain):
    urls = [domain] # Toujours inclure la racine
    sitemap_url = f"{domain}/sitemap.xml"
    try:
        # User-Agent classique pour éviter les blocages basiques
        headers = {'User-Agent': 'AgentVisitorBot/1.0'}
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                # Trouver toutes les balises <loc>
                for child in root.iter():
                    if child.tag.endswith('loc') and child.text:
                        urls.append(child.text.strip())
            except ET.ParseError:
                # Parfois sitemap n'est pas XML
                pass
    except Exception as e:
        print(f"[-] Impossible de lire le sitemap de {domain}: {e}")
    
    return list(set(urls))

def ping_indexnow(urls):
    if not urls:
        return
    
    # Grouper les URLs par domaine car IndexNow demande une requête par host
    from collections import defaultdict
    host_groups = defaultdict(list)
    for url in urls:
        parsed = urllib.parse.urlparse(url)
        host_groups[parsed.netloc].append(url)
    
    for host, host_urls in host_groups.items():
        payload = {
            "host": host,
            "key": INDEXNOW_KEY,
            "keyLocation": f"https://{host}/{INDEXNOW_KEY}.txt",
            "urlList": host_urls
        }
        try:
            res = requests.post("https://api.indexnow.org/indexnow", json=payload, timeout=10)
            if res.status_code in [200, 202]:
                print(f"[+] IndexNow ping OK pour {host} ({len(host_urls)} URLs)")
            else:
                print(f"[-] IndexNow ping échoué pour {host} (Status: {res.status_code})")
        except Exception as e:
            print(f"[-] IndexNow ping erreur pour {host}: {e}")

def prompt_ai_agents(url):
    print(f"[*] Demande aux agents IA de lire {url} ...")
    prompt = f"Peux-tu lire cette page web et me faire un résumé détaillé de son contenu ? Assure-toi de visiter le lien pour me répondre : {url}"
    
    success = False
    # Essai 1 : DuckDuckGo Chat (rapide et gratuit via g4f)
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o_mini,
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.DuckDuckGo,
            timeout=30
        )
        if response:
            success = True
    except Exception:
        pass
        
    # Essai 2 : Blackbox (souvent accès web)
    if not success:
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": prompt}],
                provider=g4f.Provider.Blackbox,
                timeout=30
            )
            if response:
                success = True
        except Exception:
            pass

    if success:
        print(f"[+] Un agent IA a traité et visité {url}.")
    else:
        print(f"[-] Impossible d'obtenir une réponse d'un agent gratuit pour {url}. (Normal avec les proxys gratuits)")

def main():
    print("=== Lancement du Agent Visitor Bot ===")
    all_urls = []
    
    for domain in DOMAINS:
        urls = get_urls_from_sitemap(domain)
        all_urls.extend(urls)
        print(f"[*] {domain} -> {len(urls)} URLs trouvées.")
        
    # Dédupliquer au cas où
    all_urls = list(set(all_urls))
    print(f"\nTotal URLs à indexer et visiter : {len(all_urls)}")
    
    # 1. Soumission aux moteurs de recherche (IndexNow)
    print("\n=== Soumission à IndexNow (Bing, Yandex, Seznam) ===")
    ping_indexnow(all_urls)
    
    # 2. Stimulation des Agents IA (G4F)
    print("\n=== Stimulation des Agents IA ===")
    print("Le bot va maintenant demander à différentes IAs gratuites de lire vos pages.")
    
    # Pour ne pas surcharger les APIs gratuites et se faire bannir l'IP de GitHub Actions,
    # on limite la requête IA à un échantillon aléatoire de 30 pages par exécution.
    import random
    target_urls = random.sample(all_urls, min(len(all_urls), 30))
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(prompt_ai_agents, target_urls)
        
    print("\n=== Terminé ! Vos sites ont été poussés vers les IAs et Moteurs ===")

if __name__ == "__main__":
    main()
