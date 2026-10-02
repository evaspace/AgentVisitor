import requests
import xml.etree.ElementTree as ET
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import g4f
import re
import os

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Agent Visitor - Automated AI Indexing Bot")
    parser.add_argument("--caddyfile", default="/etc/caddy/Caddyfile", help="Path to the Caddyfile for dynamic domain extraction")
    parser.add_argument("--indexnow-key", default=os.environ.get("INDEXNOW_KEY", ""), help="IndexNow API key (or set INDEXNOW_KEY env var)")
    return parser.parse_args()

def get_domains_from_caddyfile(caddyfile_path):
    domains = set()
    if not os.path.exists(caddyfile_path):
        print(f"[-] Caddyfile non trouvé à {caddyfile_path}. Assurez-vous d'être sur le bon serveur ou spécifiez --caddyfile.")
        return []
    
    with open(caddyfile_path, 'r') as f:
        content = f.read()
    
    # Trouver tous les blocs de domaines dans le Caddyfile.
    # Ex: pierref.eu, morgan.pierref.eu {
    # ou: opticars.pierref.eu {
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # On cherche une ligne qui contient '.eu' et se termine par '{'
        if '{' in line and '.eu' in line and not line.startswith('#'):
            # Nettoyer la ligne pour extraire les domaines
            block_def = line.split('{')[0].strip()
            # Séparer s'il y a des virgules
            for dom in block_def.split(','):
                dom = dom.strip()
                if dom.endswith('.eu'):
                    domains.add(f"https://{dom}")
    return list(domains)

def get_urls_from_sitemap(domain):
    urls = [domain]
    sitemap_url = f"{domain}/sitemap.xml"
    try:
        headers = {'User-Agent': 'AgentVisitorBot/1.0'}
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                for child in root.iter():
                    if child.tag.endswith('loc') and child.text:
                        urls.append(child.text.strip())
            except ET.ParseError:
                pass
    except Exception:
        pass
    
    return list(set(urls))

def ping_indexnow(urls, indexnow_key):
    if not urls or not indexnow_key:
        if not indexnow_key:
            print("[-] Pas de clé IndexNow fournie, étape ignorée.")
        return
    
    from collections import defaultdict
    host_groups = defaultdict(list)
    for url in urls:
        parsed = urllib.parse.urlparse(url)
        host_groups[parsed.netloc].append(url)
    
    for host, host_urls in host_groups.items():
        payload = {
            "host": host,
            "key": indexnow_key,
            "keyLocation": f"https://{host}/{indexnow_key}.txt",
            "urlList": host_urls
        }
        try:
            res = requests.post("https://api.indexnow.org/indexnow", json=payload, timeout=10)
            if res.status_code in [200, 202]:
                print(f"[+] IndexNow ping OK pour {host} ({len(host_urls)} URLs)")
            else:
                print(f"[-] IndexNow ping échoué pour {host} (Status: {res.status_code})")
        except Exception:
            pass

def prompt_ai_agents(url):
    print(f"[*] Demande aux agents IA de lire {url} ...")
    prompt = f"Peux-tu lire cette page web et me faire un résumé détaillé de son contenu ? Assure-toi de visiter le lien pour me répondre : {url}"
    
    providers = [
        (g4f.models.gpt_4o_mini, g4f.Provider.DuckDuckGo),
        (g4f.models.gpt_4o, g4f.Provider.Blackbox),
        (g4f.models.claude_3_5_sonnet, g4f.Provider.Blackbox),
        (g4f.models.gemini_1_5_pro, g4f.Provider.Blackbox),
        (g4f.models.llama_3_70b, g4f.Provider.DeepInfraChat),
        (g4f.models.mixtral_8x7b, g4f.Provider.DeepInfraChat),
        (g4f.models.command_r_plus, g4f.Provider.HuggingChat),
        (g4f.models.qwen_2_72b, g4f.Provider.HuggingChat),
        (g4f.models.gpt_35_turbo, g4f.Provider.ChatgptFree)
    ]
    
    success_count = 0
    for model, provider in providers:
        try:
            response = g4f.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                provider=provider,
                timeout=15
            )
            if response:
                success_count += 1
                print(f"  [+] Un agent ({model.name}) a visité {url}.")
        except Exception:
            pass

    if success_count > 0:
        print(f"[+] Total de {success_count} agents IA ont visité {url}.")
    else:
        print(f"[-] Impossible d'obtenir une réponse d'un agent gratuit pour {url}.")

def main():
    args = get_args()
    print("=== Lancement du Agent Visitor Bot (Mode Serveur One-Shot) ===")
    
    # 1. Extraction dynamique des domaines depuis Caddyfile
    print("\n[*] Lecture dynamique du Caddyfile...")
    domains = get_domains_from_caddyfile(args.caddyfile)
    if not domains:
        print("Aucun domaine trouvé, arrêt du bot.")
        return
        
    print(f"[+] {len(domains)} domaines détectés automatiquement !")
    for d in domains:
        print(f"  - {d}")
        
    all_urls = []
    
    for domain in domains:
        urls = get_urls_from_sitemap(domain)
        all_urls.extend(urls)
        
    all_urls = list(set(all_urls))
    print(f"\nTotal URLs à indexer et visiter : {len(all_urls)}")
    
    # 2. Soumission aux moteurs de recherche (IndexNow)
    print("\n=== Soumission à IndexNow (Bing, Yandex, Seznam) ===")
    ping_indexnow(all_urls, args.indexnow_key)
    
    # 3. Stimulation des Agents IA (G4F)
    print("\n=== Stimulation des Agents IA ===")
    
    # Limiter aléatoirement pour ne pas tout bloquer d'un coup
    import random
    target_urls = random.sample(all_urls, min(len(all_urls), 30))
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(prompt_ai_agents, target_urls)
        
    print("\n=== Terminé ! Vos sites ont été poussés vers les IAs et Moteurs ===")

if __name__ == "__main__":
    main()
