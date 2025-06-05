#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil de traduction de fichiers SRT utilisant Ollama
"""

import re
import sys
import argparse
import requests
import json
from pathlib import Path

class SRTTranslator:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "gemma3:12b"
    
    def parse_srt(self, srt_content):
        """Parse le contenu du fichier SRT"""
        # Pattern pour extraire les blocs SRT
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\d+\n|\n*$)'
        matches = re.findall(pattern, srt_content, re.DOTALL)
        
        entries = []
        for match in matches:
            number = match[0]
            timestamp = match[1]
            text = match[2].strip()
            entries.append({
                'number': number,
                'timestamp': timestamp,
                'text': text
            })
        
        return entries
    
    def translate_text(self, text, source_lang, target_lang):
        """Traduit un texte en utilisant Ollama"""
        prompt = f"""Traduis ce texte de {source_lang} vers {target_lang}. 
Réponds UNIQUEMENT avec la traduction, sans explication ni commentaire.

Texte à traduire: {text}"""

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.ollama_url}/api/generate", json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result['response'].strip()
            else:
                print(f"Erreur API: {response.status_code}")
                return text
        except Exception as e:
            print(f"Erreur lors de la traduction: {e}")
            return text
    
    def translate_srt_file(self, input_file, output_file, source_lang, target_lang):
        """Traduit un fichier SRT complet"""
        # Lire le fichier SRT
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Essayer avec d'autres encodages
            try:
                with open(input_file, 'r', encoding='cp1252') as f:
                    content = f.read()
            except:
                with open(input_file, 'r', encoding='latin-1') as f:
                    content = f.read()
        
        # Parser le contenu
        entries = self.parse_srt(content)
        
        if not entries:
            print("Aucune entrée SRT trouvée dans le fichier.")
            return
        
        print(f"Traduction de {len(entries)} entrées...")
        
        # Traduire chaque entrée
        translated_entries = []
        for i, entry in enumerate(entries, 1):
            print(f"Traduction {i}/{len(entries)}: {entry['text'][:50]}...")
            
            translated_text = self.translate_text(
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
        
        print(f"Traduction terminée ! Fichier sauvegardé : {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Traducteur de fichiers SRT utilisant Ollama")
    parser.add_argument("input", help="Fichier SRT d'entrée")
    parser.add_argument("output", help="Fichier SRT de sortie")
    parser.add_argument("--source", "-s", default="anglais", help="Langue source (défaut: anglais)")
    parser.add_argument("--target", "-t", default="français", help="Langue cible (défaut: français)")
    parser.add_argument("--url", default="http://localhost:11434", help="URL Ollama (défaut: http://localhost:11434)")
    
    args = parser.parse_args()
    
    # Vérifier que le fichier d'entrée existe
    if not Path(args.input).exists():
        print(f"Erreur: Le fichier {args.input} n'existe pas.")
        sys.exit(1)
    
    # Créer le traducteur
    translator = SRTTranslator(args.url)
    
    # Test de connexion à Ollama
    try:
        response = requests.get(f"{args.url}/api/tags", timeout=5)
        if response.status_code != 200:
            print("Erreur: Impossible de se connecter à Ollama. Assurez-vous qu'il est démarré.")
            sys.exit(1)
    except:
        print("Erreur: Ollama n'est pas accessible. Vérifiez qu'il est démarré sur", args.url)
        sys.exit(1)
    
    # Traduire le fichier
    translator.translate_srt_file(args.input, args.output, args.source, args.target)

if __name__ == "__main__":
    main() 