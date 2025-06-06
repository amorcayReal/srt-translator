@echo off
echo 🎬 Lancement du Traducteur SRT - Interface Streamlit
echo ====================================================
echo.
echo 📋 Verification des dependances...

python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit non trouve. Installation...
    pip install streamlit
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation de Streamlit
        pause
        exit /b 1
    )
)

echo ✅ Streamlit pret !
echo.
echo 🚀 Lancement de l'interface...
echo 🌐 L'application s'ouvrira dans votre navigateur
echo 📍 URL: http://localhost:8501
echo.
echo ⏹️  Pour arreter l'application: Ctrl+C
echo.

python -m streamlit run streamlit_app.py --server.port 8501 --server.address localhost

echo.
echo 👋 Application fermee. Appuyez sur une touche pour quitter...
pause >nul 