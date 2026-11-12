import os
import requests

# Configura i dati della tua repository GitHub
owner = "samu-saba"
repo = "CRrT"
branch = "main"
folder = "bassi"

api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder}?ref={branch}"

def get_github_contents(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>Archivio Studio Permanente - Sezione Bassi</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #ffffff; color: #222222; }
        header { margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #1a365d; }
        h1 { margin: 0 0 5px 0; color: #1a365d; font-size: 1.8rem; }
        p.subtitle { margin: 0; color: #555555; font-size: 0.95rem; }
        .search-container { margin-bottom: 25px; }
        #search-input { width: 100%; padding: 12px 15px; font-size: 1rem; border: 2px solid #cccccc; border-radius: 6px; outline: none; box-sizing: border-box; }
        .section { margin-bottom: 20px; border: 1px solid #cccccc; border-radius: 6px; overflow: hidden; background-color: #fafafa; }
        details { width: 100%; }
        summary { background-color: #1a365d; color: #ffffff; font-size: 1.2rem; font-weight: bold; padding: 15px 20px; cursor: pointer; user-select: none; list-style: none; }
        summary::-webkit-details-marker { display: none; }
        summary::after { content: ' ▼'; font-size: 0.9rem; float: right; }
        details[open] summary::after { transform: rotate(180deg); }
        .section-content { padding: 20px; background-color: #ffffff; border-top: 1px solid #cccccc; }
        .track { margin-bottom: 15px; display: flex; flex-direction: column; }
        .track-title { font-weight: bold; margin-bottom: 5px; color: #333333; font-size: 0.95rem; }
        audio { width: 100%; height: 40px; }
    </style>
</head>
<body>
    <header>
        <h1>Archivio Studio Permanente – Sezione Bassi</h1>
        <p class="subtitle">Libreria completa di tutti i brani – Riproduzione sequenziale continua</p>
    </header>
    <div class="search-container">
        <input type="text" id="search-input" placeholder="🔍 Cerca un brano...">
    </div>
    <div id="playlist-container">
"""

items = get_github_contents(api_url)

# Esplora la cartella principale di bassi
for item in items:
    if item['type'] == 'dir':
        dir_name = item['name']
        sub_items = get_github_contents(item['url'])
        
        tracks_html = ""
        for sub in sub_items:
            # Se trova file audio direttamente o dentro sottocartelle
            if sub['type'] == 'file' and sub['name'].lower().endswith(('.mp3', '.m4a', '.wav')):
                file_url = sub['download_url']
                file_name = sub['name']
                tracks_html += f"""
                    <div class="track" data-title="{file_name.lower()}">
                        <span class="track-title">{file_name}</span>
                        <audio controls controlsList="nodownload" class="global-audio" src="{file_url}"></audio>
                    </div>"""
            elif sub['type'] == 'dir':
                # Gestisce il secondo livello di sottocartelle (es. nomecartella/nomecartella)
                nested_items = get_github_contents(sub['url'])
                for nest in nested_items:
                    if nest['type'] == 'file' and nest['name'].lower().endswith(('.mp3', '.m4a', '.wav')):
                        file_url = nest['download_url']
                        file_name = nest['name']
                        tracks_html += f"""
                            <div class="track" data-title="{file_name.lower()}">
                                <span class="track-title">{file_name}</span>
                                <audio controls controlsList="nodownload" class="global-audio" src="{file_url}"></audio>
                            </div>"""

        if tracks_html:
            html_content += f"""
        <div class="section" data-section-name="{dir_name}">
            <details>
                <summary>📁 {dir_name}</summary>
                <div class="section-content">{tracks_html}
                </div>
            </details>
        </div>"""

html_content += """
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const allAudioElements = Array.from(document.querySelectorAll('.global-audio'));
            const searchInput = document.getElementById('search-input');
            const sections = document.querySelectorAll('.section');

            allAudioElements.forEach((audio, index) => {
                audio.addEventListener('contextmenu', e => e.preventDefault());
                audio.addEventListener('ended', () => {
                    for (let i = index + 1; i < allAudioElements.length; i++) {
                        if (allAudioElements[i].closest('.track').style.display !== 'none') {
                            allAudioElements[i].play();
                            break;
                        }
                    }
                });
                audio.addEventListener('play', () => {
                    allAudioElements.forEach(o => { if (o !== audio) o.pause(); });
                });
            });

            searchInput.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase().trim();
                sections.forEach(section => {
                    const tracks = section.querySelectorAll('.track');
                    let visible = 0;
                    tracks.forEach(track => {
                        const title = track.getAttribute('data-title') || '';
                        if (title.includes(term)) {
                            track.style.display = 'flex';
                            visible++;
                        } else {
                            track.style.display = 'none';
                        }
                    });
                    const details = section.querySelector('details');
                    if (visible > 0) {
                        section.style.display = 'block';
                        if (term !== '') details.setAttribute('open', 'open');
                    } else {
                        section.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("File index.html generato con successo!")