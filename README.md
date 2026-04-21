# KilaKochen - Kochplaner für den Kinderladen

KilaKochen ist eine Flask-basierte Webapplikation zur Verwaltung und Bereitstellung von Kochplänen für einen Kinderladen. Die Anwendung ermöglicht es, Rezepte zu verwalten, Wochenpläne zu erstellen und diese als PDF zu exportieren.

Diese Applikation ist der Nachfolger einer ursprünglichen PHP-Implementierung.

## Features

- **Wochenplan-Verwaltung:** Erstellung und Bearbeitung von Speiseplänen für die gesamte Woche.
- **Rezept-Datenbank:** Speicherung von Rezepten inklusive Kategorien (Hauptspeise, Beilage, Nachtisch).
- **Allergen-Management:** Verfolgung von Allergenen in Rezepten und Zutaten.
- **PDF-Export:** Generierung von druckbaren Wochenplänen als PDF (via WeasyPrint).
- **Statistiken:** Übersicht über die Häufigkeit der verwendeten Rezepte.
- **Benutzerverwaltung & Sicherheit:** Authentifizierungssystem für Administratoren und Köche mit rollenbasierter Zugriffskontrolle und Schutz kritischer Funktionen.
- **Einkaufsliste:** Unterstützung bei der Erstellung von Einkaufslisten basierend auf den Plänen.

## Technologien

- **Backend:** Python mit [Flask](https://flask.palletsprojects.com/)
- **Datenbank:** SQLAlchemy (standardmäßig SQLite, MySQL-Unterstützung via PyMySQL vorhanden)
- **Frontend:** Jinja2 Templates mit Bootstrap (via Flask-Bootstrap)
- **Formulare:** Flask-WTF
- **Migrationen:** Flask-Migrate (Alembic)
- **PDF-Erzeugung:** Flask-WeasyPrint

## Installation

### Voraussetzungen

- Python 3.8+
- pip (Python Paketmanager)

### Schritte

1. Repository klonen oder herunterladen.
2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. Datenbank initialisieren:
   ```bash
   flask db upgrade
   ```

## Konfiguration

Die Anwendung nutzt Umgebungsvariablen für die Konfiguration. Diese können in einer `.env`-Datei im Wurzelverzeichnis hinterlegt werden. **Hinweis:** Ein fehlender `SECRET_KEY` führt dazu, dass die Anwendung aus Sicherheitsgründen nicht startet.

- `SECRET_KEY`: **Erforderlich.** Ein langer, zufälliger String für die Sitzungssicherheit.
- `DATABASE_URL`: Verbindungs-String für die Datenbank (z.B. `sqlite:///app.db` oder `mysql+pymysql://user:pass@host/db`).
- `MAIL_SERVER`, `MAIL_PORT`, etc.: Einstellungen für den E-Mail-Versand.
- `FLASK_APP`: Sollte auf `kilakochen` gesetzt sein.
- `FLASK_DEBUG`: Aktiviert den Debug-Modus (standardmäßig `false` in `.flaskenv` für maximale Sicherheit).

## Starten der Anwendung

Im aktivierten virtuellen Umfeld:

```bash
flask run
```

Die Anwendung ist standardmäßig unter `http://127.0.0.1:5000` erreichbar.

## Projektstruktur

- `kilakochen/`: Hauptpaket der Anwendung.
  - `auth/`: Authentifizierung (Login/Logout).
  - `recipe/`: Verwaltung von Rezepten.
  - `ingredient/`: Verwaltung von Zutaten.
  - `main/`: Hauptlogik (Wochenpläne, Index, Statistiken).
  - `models.py`: Datenbankmodelle.
  - `templates/`: HTML-Templates.
- `migrations/`: Datenbank-Migrationsskripte.
- `tests/`: Automatisierte Tests.
