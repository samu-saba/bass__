import os
from urllib.parse import quote

# Il percorso locale della cartella bassi
local_base_path = r"F:\Progetti Git\CRrT\bassi"
# Il percorso di output esatto richiesto per l'index.html
output_path = r"C:\Users\samue\Downloads\bass__\index.html"

owner = "samu-saba"
repo = "CRrT"
branch = "main"

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
        #search-input:focus { border-color: #1a365d; }
        .section { margin-bottom: 20px; border: 1px solid #cccccc; border-radius: 6px; overflow: hidden; background-color: #fafafa; }
        details { width: 100%; }
        summary { background-color: #1a365d; color: #ffffff; font-size: 1.2rem; font-weight: bold; padding: 15px 20px; cursor: pointer; user-select: none; list-style: none; }
        summary::-webkit-details-marker { display: none; }
        summary::after { content: ' ▼'; font-size: 0.9rem; float: right; transition: transform 0.2s; }
        details[open] summary::after { transform: rotate(180deg); }
        .section-content { padding: 20px; background-color: #ffffff; border-top: 1px solid #cccccc; }
        .track { margin-bottom: 15px; display: flex; flex-direction: column; }
        .track:last-child { margin-bottom: 0; }
        .track-title { font-weight: bold; margin-bottom: 5px; color: #333333; font-size: 0.95rem; }
        audio { width: 100%; height: 40px; }
    </style>
</head>
<body>
    <header>
        <h1>Archivio Studio Permanente – Sezione Bassi</h1>
        <p class="subtitle">Libreria completa – Riproduzione sequenziale continua ininterrotta</p>
    </header>
    <div class="search-container">
        <input type="text" id="search-input" placeholder="🔍 Cerca un brano o una cartella...">
    </div>
    <div id="playlist-container">
"""

if not os.path.exists(local_base_path):
    print(f"Errore: Il percorso sorgente '{local_base_path}' non esiste o non è accessibile.")
else:
    # Crea la cartella di destinazione se non esiste
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for root, dirs, files in os.walk(local_base_path):
        dirs.sort()
        files.sort()
        audio_files = [f for f in files if f.lower().endswith(('.mp3', '.m4a', '.wav'))]
        if audio_files:
            folder_name = os.path.basename(root)
            tracks_html = ""
            for file_name in audio_files:
                rel_path = os.path.relpath(os.path.join(root, file_name), local_base_path).replace("\\", "/")
                encoded_rel_path = "/".join([quote(p) for p in rel_path.split("/")])
                file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/bassi/{encoded_rel_path}"
                
                tracks_html += f"""
                    <div class="track" data-title="{file_name.lower()}">
                        <span class="track-title">{file_name}</span>
                        <audio controls controlsList="nodownload" class="global-audio" src="{file_url}"></audio>
                    </div>"""
                    
            html_content += f"""
        <div class="section" data-section-name="{folder_name}">
            <details>
                <summary>📁 {folder_name}</summary>
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

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"File index.html generato con successo esattamente in: {output_path}")