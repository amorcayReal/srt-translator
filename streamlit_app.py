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
import zipfile
import io
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
        'upload_mode': 'Mode de traitement',
        'single_file': 'Fichier unique',
        'batch_files': 'Traitement en série',
        'choose_file': 'Choisissez votre fichier SRT',
        'choose_files': 'Choisissez vos fichiers SRT',
        'choose_file_help': 'Sélectionnez le fichier de sous-titres à traduire',
        'choose_files_help': 'Sélectionnez plusieurs fichiers de sous-titres à traduire',
        'file_loaded': '✅ Fichier chargé: **{}** ({} octets)',
        'files_loaded': '✅ {} fichiers chargés (Total: {} octets)',
        'batch_processing': '🔄 Traitement en série ({}/{}): {}',
        'batch_completed': '🎉 Traitement en série terminé ! {} fichiers traduits.',
        'batch_success': '✅ Tous les fichiers ont été traduits avec succès !',
        'initializing': 'Initialisation...',
        'download_all': '📦 Télécharger tous les fichiers (ZIP)',
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
        'cancel_translation': '🛑 Annuler la traduction',
        'translation_cancelled': '⚠️ Traduction annulée par l\'utilisateur',
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
        'upload_mode': 'Processing Mode',
        'single_file': 'Single File',
        'batch_files': 'Batch Processing',
        'choose_file': 'Choose your SRT file',
        'choose_files': 'Choose your SRT files',
        'choose_file_help': 'Select the subtitle file to translate',
        'choose_files_help': 'Select multiple subtitle files to translate',
        'file_loaded': '✅ File loaded: **{}** ({} bytes)',
        'files_loaded': '✅ {} files loaded (Total: {} bytes)',
        'batch_processing': '🔄 Batch processing ({}/{}): {}',
        'batch_completed': '🎉 Batch processing completed! {} files translated.',
        'batch_success': '✅ All files have been successfully translated!',
        'initializing': 'Initializing...',
        'download_all': '📦 Download all files (ZIP)',
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
        'cancel_translation': '🛑 Cancel translation',
        'translation_cancelled': '⚠️ Translation cancelled by user',
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

def process_single_file(file, translator, source_lang, target_lang, ui_lang, progress_callback=None, cancel_callback=None):
    """Traite un seul fichier SRT avec callbacks de progression et annulation"""
    # Créer des fichiers temporaires
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.srt', delete=False) as input_temp:
        input_temp.write(file.read())
        input_temp_path = input_temp.name
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.srt', delete=False, encoding='utf-8') as output_temp:
        output_temp_path = output_temp.name
    
    # Réinitialiser le pointeur du fichier
    file.seek(0)
    
    try:
        # Lire et parser le fichier
        try:
            with open(input_temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(input_temp_path, 'r', encoding='cp1252') as f:
                    content = f.read()
            except:
                with open(input_temp_path, 'r', encoding='latin-1') as f:
                    content = f.read()
        
        entries = translator.parse_srt(content)
        
        if not entries:
            return None, get_text("no_entries_found", ui_lang)
        
        # Traduire chaque entrée avec progression
        translated_entries = []
        for i, entry in enumerate(entries):
            # Vérifier l'annulation
            if cancel_callback and cancel_callback():
                return None, get_text("translation_cancelled", ui_lang)
            
            # Mise à jour de la progression
            if progress_callback:
                progress_callback(i, len(entries), entry['text'][:50])
            
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
        with open(output_temp_path, 'w', encoding='utf-8') as f:
            for entry in translated_entries:
                f.write(f"{entry['number']}\n")
                f.write(f"{entry['timestamp']}\n")
                f.write(f"{entry['text']}\n\n")
        
        # Lire le contenu traduit
        with open(output_temp_path, 'r', encoding='utf-8') as f:
            translated_content = f.read()
        
        return translated_content, None
        
    finally:
        # Nettoyage
        try:
            os.unlink(input_temp_path)
            os.unlink(output_temp_path)
        except:
            pass

def create_zip_from_files(files_data, target_lang):
    """Crée un fichier ZIP contenant tous les fichiers traduits"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for original_name, translated_content in files_data:
            # Créer le nom de fichier de sortie
            name_without_ext = Path(original_name).stem
            output_filename = f"{name_without_ext}-{target_lang.upper()}.srt"
            
            # Ajouter le fichier au ZIP
            zip_file.writestr(output_filename, translated_content)
    
    zip_buffer.seek(0)
    return zip_buffer

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
        
        # Sélecteur de mode de traitement
        processing_mode = st.radio(
            get_text("upload_mode", ui_lang),
            options=["single", "batch"],
            format_func=lambda x: get_text("single_file", ui_lang) if x == "single" else get_text("batch_files", ui_lang),
            horizontal=True
        )
        
        # Zone d'upload selon le mode
        if processing_mode == "single":
            uploaded_files = st.file_uploader(
                get_text("choose_file", ui_lang),
                type=['srt'],
                help=get_text("choose_file_help", ui_lang)
            )
            # Convertir en liste pour uniformiser le traitement
            if uploaded_files:
                uploaded_files = [uploaded_files]
        else:
            uploaded_files = st.file_uploader(
                get_text("choose_files", ui_lang),
                type=['srt'],
                accept_multiple_files=True,
                help=get_text("choose_files_help", ui_lang)
            )
        
        if uploaded_files:
            # Affichage des informations des fichiers
            if len(uploaded_files) == 1:
                file = uploaded_files[0]
                st.success(get_text("file_loaded", ui_lang).format(file.name, file.size))
            else:
                total_size = sum(f.size for f in uploaded_files)
                st.success(get_text("files_loaded", ui_lang).format(len(uploaded_files), total_size))
                
                # Afficher la liste des fichiers
                with st.expander(f"📋 {len(uploaded_files)} fichiers sélectionnés", expanded=False):
                    for i, file in enumerate(uploaded_files, 1):
                        st.write(f"{i}. **{file.name}** ({file.size} octets)")
            
            # Prévisualisation du contenu (premier fichier seulement)
            if len(uploaded_files) == 1:
                with st.expander(get_text("preview_file", ui_lang), expanded=False):
                    try:
                        content = uploaded_files[0].read().decode('utf-8')
                        uploaded_files[0].seek(0)  # Reset file pointer
                        
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
                
                # Créer le traducteur
                translator = SRTTranslator(ollama_url)
                translator.model = model_name
                
                if len(uploaded_files) == 1:
                    # Traitement d'un seul fichier
                    try:
                        file = uploaded_files[0]
                        
                        # Parser le fichier pour connaître le nombre d'entrées
                        file_content = file.read().decode('utf-8')
                        file.seek(0)
                        entries = translator.parse_srt(file_content)
                        
                        if not entries:
                            st.error(get_text("no_entries_found", ui_lang))
                            return
                        
                        # Initialiser l'état d'annulation
                        if 'cancel_translation' not in st.session_state:
                            st.session_state.cancel_translation = False
                        
                        # Interface de progression
                        progress_container = st.container()
                        with progress_container:
                            col_progress, col_cancel = st.columns([4, 1])
                            
                            with col_progress:
                                progress_bar = st.progress(0)
                                status_text = st.empty()
                                status_text.text(get_text("entries_found", ui_lang).format(len(entries)))
                            
                            with col_cancel:
                                if st.button(get_text("cancel_translation", ui_lang), type="secondary", use_container_width=True):
                                    st.session_state.cancel_translation = True
                                    st.rerun()
                        
                        # Callbacks pour la progression et l'annulation
                        def update_progress(current, total, current_text):
                            progress = (current + 1) / total
                            progress_bar.progress(progress)
                            # Affichage détaillé : "5/342 : <texte>"
                            status_text.text(f"{current + 1}/{total} : {current_text}")
                        
                        def check_cancel():
                            return st.session_state.get('cancel_translation', False)
                        
                        # Traiter le fichier avec progression en temps réel
                        translated_content, error = process_single_file(
                            file, translator, source_lang, target_lang, ui_lang,
                            progress_callback=update_progress,
                            cancel_callback=check_cancel
                        )
                        
                        if error:
                            if "annulée" in error or "cancelled" in error:
                                st.warning(error)
                                st.session_state.cancel_translation = False
                            else:
                                st.error(error)
                            return
                        
                        progress_bar.progress(1.0)
                        status_text.text(get_text("translation_completed", ui_lang))
                        
                        # Stocker dans la session
                        st.session_state['translated_content'] = translated_content
                        st.session_state['original_filename'] = file.name
                        st.session_state['processing_mode'] = 'single'
                        st.session_state.cancel_translation = False
                        
                        st.success(get_text("translation_success", ui_lang))
                        
                    except Exception as e:
                        st.error(get_text("translation_error", ui_lang).format(str(e)))
                        st.session_state.cancel_translation = False
                
                else:
                    # Traitement en lot
                    try:
                        # Initialiser l'état d'annulation
                        if 'cancel_translation' not in st.session_state:
                            st.session_state.cancel_translation = False
                        
                        # Interface de progression
                        progress_container = st.container()
                        with progress_container:
                            col_progress, col_cancel = st.columns([4, 1])
                            
                            with col_progress:
                                progress_bar = st.progress(0)
                                file_status = st.empty()  # Pour afficher le fichier en cours
                                status_text = st.empty()  # Pour afficher la progression détaillée
                            
                            with col_cancel:
                                if st.button(get_text("cancel_translation", ui_lang), type="secondary", use_container_width=True, key="cancel_batch"):
                                    st.session_state.cancel_translation = True
                                    st.rerun()
                        
                        translated_files_data = []
                        total_files = len(uploaded_files)
                        
                        for i, file in enumerate(uploaded_files):
                            # Vérifier l'annulation
                            if st.session_state.get('cancel_translation', False):
                                st.warning(get_text("translation_cancelled", ui_lang))
                                st.session_state.cancel_translation = False
                                return
                            
                            # Callback pour vérifier l'annulation pendant la traduction du fichier
                            def check_cancel():
                                return st.session_state.get('cancel_translation', False)
                            
                            # Callback pour la progression détaillée de chaque fichier
                            def update_detailed_progress(current_entry, total_entries, current_text):
                                # Progression globale des fichiers
                                file_progress = i / total_files
                                # Progression interne du fichier actuel
                                entry_progress = (current_entry + 1) / total_entries if total_entries > 0 else 0
                                # Progression combinée
                                combined_progress = (i + entry_progress) / total_files
                                
                                progress_bar.progress(combined_progress)
                                # Affichage du fichier en cours
                                file_status.text(get_text("batch_processing", ui_lang).format(i+1, total_files, file.name))
                                # Affichage détaillé : "5/342 : <texte>"
                                status_text.text(f"{current_entry + 1}/{total_entries} : {current_text}")
                            
                            # Mise à jour initiale
                            file_status.text(get_text("batch_processing", ui_lang).format(i+1, total_files, file.name))
                            status_text.text(get_text("initializing", ui_lang))
                            
                            # Traiter le fichier avec progression détaillée
                            translated_content, error = process_single_file(
                                file, translator, source_lang, target_lang, ui_lang,
                                progress_callback=update_detailed_progress,
                                cancel_callback=check_cancel
                            )
                            
                            if error:
                                if "annulée" in error or "cancelled" in error:
                                    st.warning(get_text("translation_cancelled", ui_lang))
                                    st.session_state.cancel_translation = False
                                    return
                                else:
                                    st.warning(f"⚠️ Erreur avec {file.name}: {error}")
                                    continue
                            
                            translated_files_data.append((file.name, translated_content))
                        
                        progress_bar.progress(1.0)
                        file_status.text("🎉 " + get_text("batch_completed", ui_lang).format(len(translated_files_data)))
                        status_text.text(get_text("batch_success", ui_lang))
                        
                        # Stocker dans la session
                        st.session_state['translated_files_data'] = translated_files_data
                        st.session_state['processing_mode'] = 'batch'
                        st.session_state['target_lang'] = target_lang
                        st.session_state.cancel_translation = False
                        
                        st.success(get_text("batch_completed", ui_lang).format(len(translated_files_data)))
                        
                    except Exception as e:
                        st.error(get_text("translation_error", ui_lang).format(str(e)))
                        st.session_state.cancel_translation = False
    
    with col2:
        st.header(get_text("result_section", ui_lang))
        
        # Vérifier le mode de traitement
        processing_mode = st.session_state.get('processing_mode', 'single')
        
        if processing_mode == 'single' and 'translated_content' in st.session_state and st.session_state['translated_content']:
            # Traitement d'un seul fichier
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
            output_filename = f"{name_without_ext}-{target_lang.upper()}.srt"
            
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
        
        elif processing_mode == 'batch' and 'translated_files_data' in st.session_state and st.session_state['translated_files_data']:
            # Traitement en lot
            files_data = st.session_state['translated_files_data']
            batch_target_lang = st.session_state.get('target_lang', target_lang)
            
            st.success(get_text("batch_completed", ui_lang).format(len(files_data)))
            
            # Liste des fichiers traduits
            with st.expander(f"📋 {len(files_data)} fichiers traduits", expanded=True):
                for i, (original_name, _) in enumerate(files_data, 1):
                    name_without_ext = Path(original_name).stem
                    output_name = f"{name_without_ext}-{batch_target_lang.upper()}.srt"
                    st.write(f"{i}. **{output_name}**")
            
            # Aperçu du premier fichier
            if files_data:
                with st.expander(get_text("preview_translation", ui_lang), expanded=False):
                    first_file_content = files_data[0][1]
                    lines = first_file_content.split('\n')[:15]
                    st.code('\n'.join(lines), language='text')
                    
                    if len(first_file_content.split('\n')) > 15:
                        st.info(get_text("preview_truncated", ui_lang))
            
            # Bouton de téléchargement ZIP
            if st.button(get_text("download_all", ui_lang), type="primary", use_container_width=True):
                # Créer le ZIP
                zip_buffer = create_zip_from_files(files_data, batch_target_lang)
                
                # Bouton de téléchargement
                st.download_button(
                    label="📦 Télécharger le fichier ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"subtitles-{batch_target_lang.upper()}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            
            # Statistiques
            st.subheader(get_text("statistics", ui_lang))
            total_lines = sum(len([line for line in content.split('\n') if line.strip()]) for _, content in files_data)
            total_entries = sum(content.count('\n\n') for _, content in files_data)
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Fichiers traduits", len(files_data))
            with col_stat2:
                st.metric(get_text("translated_entries", ui_lang), total_entries)
        
        else:
            st.info(get_text("upload_info", ui_lang))
            
            # Exemple d'utilisation
            with st.expander(get_text("usage_guide", ui_lang)):
                st.markdown(get_text("usage_steps", ui_lang))

if __name__ == "__main__":
    main() 