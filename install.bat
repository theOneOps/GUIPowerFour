@echo off

REM Vérifier si Python est installé
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé.
    REM Vous pouvez ajouter une commande pour installer Python ici, si nécessaire.
    exit /b
)

REM Vérifier si pip est installé
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip n'est pas installé.
    REM Vous pouvez ajouter une commande pour installer pip ici, si nécessaire.
    exit /b
)

REM Installer les dépendances à partir de requirements.txt
pip install -r requirements.txt

REM Exécuter le script principal Python
python main.py

pause
