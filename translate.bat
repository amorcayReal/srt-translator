@echo off
echo Traducteur SRT avec Ollama
echo ========================

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo Erreur: Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
if not exist "requirements_installed.flag" (
    echo Installation des dépendances...
    pip install -r requirements.txt
    echo. > requirements_installed.flag
)

REM Si aucun argument n'est fourni, afficher l'aide
if "%~1"=="" (
    echo Usage: translate.bat fichier_entree.srt fichier_sortie.srt [langue_source] [langue_cible]
    echo.
    echo Exemples:
    echo   translate.bat video.srt video_fr.srt
    echo   translate.bat video.srt video_es.srt anglais espagnol
    echo.
    echo Langues par défaut: anglais vers français
    pause
    exit /b 1
)

REM Appeler le script Python avec les arguments
if "%~4"=="" (
    if "%~3"=="" (
        python srt_translator.py "%~1" "%~2"
    ) else (
        python srt_translator.py "%~1" "%~2" --source "%~3" --target "français"
    )
) else (
    python srt_translator.py "%~1" "%~2" --source "%~3" --target "%~4"
)

pause 