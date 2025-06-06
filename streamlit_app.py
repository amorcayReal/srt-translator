#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Streamlit pour l'outil de traduction de fichiers SRT
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import requests
import time
from srt_translator import SRTTranslator

# Dictionnaire de traductions
TRANSLATIONS = {
    'fr': {
        'title': '🎬 Traducteur de Sous-titres SRT',
        'config': '⚙️ Configuration',
        'ollama': '🤖 Ollama',
        'ollama_url': 'URL Ollama',
        'ollama_url_help': "L'URL de votre instance Ollama",
        'test_connection': '🔍 Tester la connexion',
        'testing_connection': 'Test de connexion...',
        'connection_success': '✅ Connexion réussie !',
        'models_available': '📋 Modèles disponibles: {}',
        'connection_failed': '❌ Impossible de se connecter à Ollama',
        'model_name': 'Modèle Ollama',
        'model_help': 'Nom du modèle à utiliser pour la traduction',
        'languages': '🌍 Langues',
        'source_lang': 'Langue source',
        'target_lang': 'Langue cible',
        'about': 'ℹ️ À propos',
        'about_text': '''**Traducteur SRT** vous permet de traduire facilement vos fichiers de sous-titres.

**Fonctionnalités:**
- 🚀 Traduction rapide avec Ollama
- 📁 Support des formats SRT
- 🎯 Interface intuitive
- 💾 Téléchargement direct du résultat''',
        'upload_section': '📂 Upload du fichier SRT',
        'choose_file': 'Choisissez votre fichier SRT',
        'choose_file_help': 'Sélectionnez le fichier de sous-titres à traduire',
        'file_loaded': '✅ Fichier chargé: **{}** ({} octets)',
        'preview_file': '👀 Aperçu du fichier',
        'file_truncated': '... (fichier tronqué pour l\'aperçu)',
        'encoding_warning': '⚠️ Impossible de décoder le fichier en UTF-8. La traduction tentera d\'autres encodages.',
        'start_translation': '🚀 Lancer la traduction',
        'ollama_connection_error': '❌ Impossible de se connecter à Ollama. Vérifiez votre configuration.',
        'translation_progress': '🔄 Traduction en cours...',
        'entries_found': '📋 {} entrées trouvées',
        'translating_entry': 'Traduction {}/{}: {}...',
        'translation_completed': '✅ Traduction terminée !',
        'translation_success': '🎉 Traduction terminée avec succès !',
        'translation_error': '❌ Erreur lors de la traduction: {}',
        'no_entries_found': 'Aucune entrée SRT trouvée dans le fichier.',
        'result_section': '📥 Résultat',
        'file_ready': '✅ Fichier traduit prêt !',
        'preview_translation': '👀 Aperçu de la traduction',
        'preview_truncated': '... (aperçu tronqué)',
        'download_file': '💾 Télécharger le fichier traduit',
        'statistics': '📊 Statistiques',
        'total_lines': 'Lignes totales',
        'translated_entries': 'Entrées traduites',
        'upload_info': '👆 Uploadez un fichier SRT et lancez la traduction pour voir le résultat ici',
        'usage_guide': '📖 Guide d\'utilisation',
        'usage_steps': '''**Étapes simples :**

1. **Configurer Ollama** dans la barre latérale
2. **Choisir les langues** source et cible
3. **Uploader votre fichier SRT**
4. **Cliquer sur "Lancer la traduction"**
5. **Télécharger le résultat** !

**Format SRT supporté :**
```
1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:05,000 --> 00:00:08,000
How are you today?
```''',
        'interface_language': '🌐 Langue de l\'interface'
    },
    'en': {
        'title': '🎬 SRT Subtitle Translator',
        'config': '⚙️ Configuration',
        'ollama': '🤖 Ollama',
        'ollama_url': 'Ollama URL',
        'ollama_url_help': 'The URL of your Ollama instance',
        'test_connection': '🔍 Test connection',
        'testing_connection': 'Testing connection...',
        'connection_success': '✅ Connection successful!',
        'models_available': '📋 Available models: {}',
        'connection_failed': '❌ Unable to connect to Ollama',
        'model_name': 'Ollama Model',
        'model_help': 'Name of the model to use for translation',
        'languages': '🌍 Languages',
        'source_lang': 'Source language',
        'target_lang': 'Target language',
        'about': 'ℹ️ About',
        'about_text': '''**SRT Translator** allows you to easily translate your subtitle files.

**Features:**
- 🚀 Fast translation with Ollama
- 📁 SRT format support
- 🎯 Intuitive interface
- 💾 Direct result download''',
        'upload_section': '📂 SRT File Upload',
        'choose_file': 'Choose your SRT file',
        'choose_file_help': 'Select the subtitle file to translate',
        'file_loaded': '✅ File loaded: **{}** ({} bytes)',
        'preview_file': '👀 File preview',
        'file_truncated': '... (file truncated for preview)',
        'encoding_warning': '⚠️ Unable to decode file as UTF-8. Translation will try other encodings.',
        'start_translation': '🚀 Start translation',
        'ollama_connection_error': '❌ Unable to connect to Ollama. Check your configuration.',
        'translation_progress': '🔄 Translation in progress...',
        'entries_found': '📋 {} entries found',
        'translating_entry': 'Translating {}/{}: {}...',
        'translation_completed': '✅ Translation completed!',
        'translation_success': '🎉 Translation completed successfully!',
        'translation_error': '❌ Translation error: {}',
        'no_entries_found': 'No SRT entries found in the file.',
        'result_section': '📥 Result',
        'file_ready': '✅ Translated file ready!',
        'preview_translation': '👀 Translation preview',
        'preview_truncated': '... (preview truncated)',
        'download_file': '💾 Download translated file',
        'statistics': '📊 Statistics',
        'total_lines': 'Total lines',
        'translated_entries': 'Translated entries',
        'upload_info': '👆 Upload an SRT file and start translation to see the result here',
        'usage_guide': '📖 Usage Guide',
        'usage_steps': '''**Simple steps:**

1. **Configure Ollama** in the sidebar
2. **Choose languages** source and target
3. **Upload your SRT file**
4. **Click "Start translation"**
5. **Download the result**!

**Supported SRT format:**
```
1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:05,000 --> 00:00:08,000
How are you today?
```''',
        'interface_language': '🌐 Interface Language'
    }
}

def get_text(key, lang='fr'):
    """Récupère le texte traduit selon la langue sélectionnée"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

# Configuration de la page
st.set_page_config(
    page_title="Traducteur SRT", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour personnaliser l'apparence
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #2E86AB;
    padding: 1rem 0;
    border-bottom: 2px solid #f0f2f6;
    margin-bottom: 2rem;
}

.upload-box {
    border: 2px dashed #2E86AB;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
    background-color: #f8f9fa;
}

.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}

.error-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}

.sidebar .sidebar-content {
    background-color: #f8f9fa;
}

.stProgress .st-bo {
    background-color: #2E86AB;
}
</style>
""", unsafe_allow_html=True)

def check_ollama_connection(url):
    """Vérifie la connexion à Ollama"""
    try:
        response = requests.get(f"{url}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_models(url):
    """Récupère la liste des modèles disponibles"""
    try:
        response = requests.get(f"{url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model['name'] for model in models]
        return []
    except:
        return []

def main():
    # Initialiser la langue dans session_state si elle n'existe pas
    if 'ui_language' not in st.session_state:
        st.session_state.ui_language = 'fr'
    
    # Sidebar pour la configuration
    with st.sidebar:
        # Sélecteur de langue en haut de la sidebar
        ui_lang = st.selectbox(
            "🌐 Language / Langue",
            options=['fr', 'en'],
            format_func=lambda x: "🇫🇷 Français" if x == 'fr' else "🇬🇧 English",
            index=0 if st.session_state.ui_language == 'fr' else 1,
            key="language_selector"
        )
        
        # Mettre à jour la langue si elle a changé
        if ui_lang != st.session_state.ui_language:
            st.session_state.ui_language = ui_lang
            st.rerun()
        
        st.divider()
        
        st.header(get_text("config", ui_lang))
    
        # En-tête principal
    st.markdown(f'<h1 class="main-header">{get_text("title", ui_lang)}</h1>', unsafe_allow_html=True)
    
    # Continuer avec la sidebar
    with st.sidebar:
        # Configuration d'Ollama
        st.subheader(get_text("ollama", ui_lang))
        ollama_url = st.text_input(
            get_text("ollama_url", ui_lang), 
            value="http://localhost:11434",
            help=get_text("ollama_url_help", ui_lang)
        )
        
        # Test de connexion
        if st.button(get_text("test_connection", ui_lang)):
            with st.spinner(get_text("testing_connection", ui_lang)):
                if check_ollama_connection(ollama_url):
                    st.success(get_text("connection_success", ui_lang))
                    
                    # Récupérer les modèles disponibles
                    models = get_available_models(ollama_url)
                    if models:
                        st.info(get_text("models_available", ui_lang).format(', '.join(models)))
                else:
                    st.error(get_text("connection_failed", ui_lang))
        
        # Sélection du modèle
        model_name = st.text_input(
            get_text("model_name", ui_lang), 
            value="gemma3:12b",
            help=get_text("model_help", ui_lang)
        )
        
        st.divider()
        
        # Configuration des langues
        st.subheader(get_text("languages", ui_lang))
        
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox(
                get_text("source_lang", ui_lang),
                ["anglais", "français", "espagnol", "italien", "allemand", "portugais", "chinois", "japonais", "coréen", "russe"],
                index=0
            )
        
        with col2:
            target_lang = st.selectbox(
                get_text("target_lang", ui_lang),
                ["français", "anglais", "espagnol", "italien", "allemand", "portugais", "chinois", "japonais", "coréen", "russe"],
                index=0
            )
        
        st.divider()
        
        # Informations
        st.subheader(get_text("about", ui_lang))
        st.markdown(get_text("about_text", ui_lang))
    
    # Zone principale
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header(get_text("upload_section", ui_lang))
        
        # Zone d'upload
        uploaded_file = st.file_uploader(
            get_text("choose_file", ui_lang),
            type=['srt'],
            help=get_text("choose_file_help", ui_lang)
        )
        
        if uploaded_file is not None:
            # Affichage des informations du fichier
            st.success(get_text("file_loaded", ui_lang).format(uploaded_file.name, uploaded_file.size))
            
            # Prévisualisation du contenu
            with st.expander(get_text("preview_file", ui_lang), expanded=False):
                try:
                    content = uploaded_file.read().decode('utf-8')
                    uploaded_file.seek(0)  # Reset file pointer
                    
                    # Afficher les premières lignes
                    lines = content.split('\n')[:20]
                    st.code('\n'.join(lines), language='text')
                    
                    if len(content.split('\n')) > 20:
                        st.info(get_text("file_truncated", ui_lang))
                        
                except UnicodeDecodeError:
                    st.warning(get_text("encoding_warning", ui_lang))
            
            # Bouton de traduction
            if st.button(get_text("start_translation", ui_lang), type="primary", use_container_width=True):
                # Vérifier la connexion Ollama
                if not check_ollama_connection(ollama_url):
                    st.error(get_text("ollama_connection_error", ui_lang))
                    return
                
                # Traitement de la traduction
                with st.spinner(get_text("translation_progress", ui_lang)):
                    try:
                        # Créer des fichiers temporaires
                        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.srt', delete=False) as input_temp:
                            input_temp.write(uploaded_file.read())
                            input_temp_path = input_temp.name
                        
                        with tempfile.NamedTemporaryFile(mode='w+', suffix='.srt', delete=False, encoding='utf-8') as output_temp:
                            output_temp_path = output_temp.name
                        
                        # Réinitialiser le pointeur du fichier
                        uploaded_file.seek(0)
                        
                        # Créer le traducteur
                        translator = SRTTranslator(ollama_url)
                        translator.model = model_name
                        
                        # Affichage de la progression
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Hook pour suivre la progression (modification temporaire)
                        original_translate = translator.translate_srt_file
                        
                        def translate_with_progress(input_file, output_file, source_lang, target_lang):
                            # Lire et parser le fichier
                            try:
                                with open(input_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                            except UnicodeDecodeError:
                                try:
                                    with open(input_file, 'r', encoding='cp1252') as f:
                                        content = f.read()
                                except:
                                    with open(input_file, 'r', encoding='latin-1') as f:
                                        content = f.read()
                            
                            entries = translator.parse_srt(content)
                            
                            if not entries:
                                st.error(get_text("no_entries_found", ui_lang))
                                return
                            
                            status_text.text(get_text("entries_found", ui_lang).format(len(entries)))
                            
                            # Traduire chaque entrée avec progression
                            translated_entries = []
                            for i, entry in enumerate(entries):
                                progress = (i + 1) / len(entries)
                                progress_bar.progress(progress)
                                status_text.text(get_text("translating_entry", ui_lang).format(i+1, len(entries), entry['text'][:50]))
                                
                                translated_text = translator.translate_text(
                                    entry['text'], 
                                    source_lang, 
                                    target_lang
                                )
                                
                                translated_entries.append({
                                    'number': entry['number'],
                                    'timestamp': entry['timestamp'],
                                    'text': translated_text
                                })
                            
                            # Écrire le fichier traduit
                            with open(output_file, 'w', encoding='utf-8') as f:
                                for entry in translated_entries:
                                    f.write(f"{entry['number']}\n")
                                    f.write(f"{entry['timestamp']}\n")
                                    f.write(f"{entry['text']}\n\n")
                            
                            progress_bar.progress(1.0)
                            status_text.text(get_text("translation_completed", ui_lang))
                        
                        # Lancer la traduction
                        translate_with_progress(input_temp_path, output_temp_path, source_lang, target_lang)
                        
                        # Lire le fichier traduit
                        with open(output_temp_path, 'r', encoding='utf-8') as f:
                            translated_content = f.read()
                        
                        # Stocker dans la session
                        st.session_state['translated_content'] = translated_content
                        st.session_state['original_filename'] = uploaded_file.name
                        
                        # Nettoyage
                        os.unlink(input_temp_path)
                        os.unlink(output_temp_path)
                        
                        st.success(get_text("translation_success", ui_lang))
                        
                    except Exception as e:
                        st.error(get_text("translation_error", ui_lang).format(str(e)))
                        # Nettoyage en cas d'erreur
                        try:
                            os.unlink(input_temp_path)
                            os.unlink(output_temp_path)
                        except:
                            pass
    
    with col2:
        st.header(get_text("result_section", ui_lang))
        
        if 'translated_content' in st.session_state and st.session_state['translated_content']:
            st.success(get_text("file_ready", ui_lang))
            
            # Aperçu du résultat
            with st.expander(get_text("preview_translation", ui_lang), expanded=True):
                lines = st.session_state['translated_content'].split('\n')[:15]
                st.code('\n'.join(lines), language='text')
                
                if len(st.session_state['translated_content'].split('\n')) > 15:
                    st.info(get_text("preview_truncated", ui_lang))
            
            # Nom du fichier de sortie
            original_name = st.session_state.get('original_filename', 'subtitle.srt')
            name_without_ext = Path(original_name).stem
            output_filename = f"{name_without_ext}_{target_lang}.srt"
            
            # Bouton de téléchargement
            st.download_button(
                label=get_text("download_file", ui_lang),
                data=st.session_state['translated_content'],
                file_name=output_filename,
                mime="text/plain",
                type="primary",
                use_container_width=True
            )
            
            # Statistiques
            st.subheader(get_text("statistics", ui_lang))
            lines_count = len([line for line in st.session_state['translated_content'].split('\n') if line.strip()])
            entries_count = st.session_state['translated_content'].count('\n\n')
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric(get_text("total_lines", ui_lang), lines_count)
            with col_stat2:
                st.metric(get_text("translated_entries", ui_lang), entries_count)
        
        else:
            st.info(get_text("upload_info", ui_lang))
            
            # Exemple d'utilisation
            with st.expander(get_text("usage_guide", ui_lang)):
                st.markdown(get_text("usage_steps", ui_lang))

if __name__ == "__main__":
    main() 