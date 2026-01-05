```markdown
# Agent Definition: Batcontrol Web UI Erweiterung

## Projekt-Übersicht

**Projektname:** Batcontrol  
**Ziel:** Erweiterung der bestehenden Python-Anwendung um eine Web-UI-Komponente  
**Hauptfunktion:** Optimierung von Stromkosten durch intelligente Batteriesteuerung für PV-Anlagen mit BYD-Batterien und Fronius Gen24 Wechselrichtern (oder MQTT-basierte Integrationen)

### Bestehende Architektur

- **Backend:** Python 3.11-basierte Anwendung
- **Hauptmodule:**
  - `core.py` - Hauptlogik und Steuerung
  - `inverter/` - Wechselrichter-Integrationen (Fronius, MQTT, Dummy)
  - `dynamictariff/` - Stromtarif-APIs (Tibber, Awattar, EVCC)
  - `forecastsolar/` - PV-Produktionsprognosen
  - `forecastconsumption/` - Verbrauchsprognosen
  - `logic/` - Berechnungslogik für Batteriesteuerung
  - `mqtt_api.py` - MQTT-Kommunikation
  - `evcc_api.py` - EVCC-Integration
- **Deployment:** Docker-basiert (Pflicht)
- **Konfiguration:** YAML-basiert (`batcontrol_config.yaml`)
- **Datenkommunikation:** MQTT Topics für Status und Steuerung

## Projekt-Boundaries

### In Scope

1. **Web-UI-Entwicklung**
   - React-basierte Frontend-Anwendung (TypeScript)
   - Integration in bestehende Docker-Container-Architektur
   - REST-API-Endpunkte für Frontend-Backend-Kommunikation
   - WebSocket-Support für Echtzeit-Updates (optional, Phase 4)

2. **UI-Komponenten (basierend auf Wireframes)**
   - Dashboard-Seite (`batcontrol_dashboard`)
   - Konfigurations-Editor (`configuration_editor_1`)
   - Analytics & Statistiken (`analytics_stats`)
   - Responsive Design (Mobile-First, dann Desktop)

3. **Backend-API-Erweiterung**
   - REST-Endpunkte für Konfiguration (GET/PUT)
   - REST-Endpunkte für Status-Daten
   - REST-Endpunkte für historische Daten
   - REST-Endpunkte für Steuerungsbefehle

4. **Testing**
   - Unit-Tests für alle neuen Komponenten
   - Integration-Tests für API-Endpunkte
   - Frontend-Tests (React Testing Library)
   - Code Coverage: **90% Minimum** für alle neuen Code-Pfade

5. **Security**
   - Authentifizierung und Autorisierung
   - Input-Validierung und Sanitization
   - Secure API-Kommunikation
   - Docker Security Best Practices

6. **Dokumentation**
   - API-Dokumentation
   - Deployment-Anleitung
   - Entwickler-Dokumentation

### Out of Scope

1. **Bestehende Backend-Logik**
   - Keine Änderungen an der Kern-Batteriesteuerungslogik (`logic/`)
   - Keine Änderungen an Wechselrichter-Treibern (außer notwendige API-Erweiterungen)
   - Keine Änderungen an Forecast-Modulen (außer API-Zugriff)

2. **Externe Integrationen**
   - Keine neuen Wechselrichter-Treiber
   - Keine neuen Tarif-APIs
   - Keine neuen Forecast-Quellen

3. **Mobile Apps**
   - Keine native iOS/Android-Apps
   - Nur responsive Web-UI

4. **Erweiterte Features (außerhalb MVP)**
   - Multi-User-Support
   - Benutzer-Management
   - Erweiterte Reporting-Features (außerhalb Wireframes)

## Docker-Pflicht

### Anforderungen

1. **Container-Architektur**
   - Web-UI muss in Docker-Container deploybar sein
   - Integration in bestehende `docker-compose.yml`
   - Multi-Stage Build für optimierte Image-Größe
   - Alpine-basierte Images bevorzugt (wie bestehendes Backend)

2. **Container-Konfiguration**
   - Environment-Variablen für Konfiguration
   - Volume-Mounts für Config und Logs (konsistent mit Backend)
   - Netzwerk-Integration mit bestehendem Backend
   - Health-Checks implementieren

3. **Deployment**
   - Docker Compose für lokale Entwicklung
   - Production-ready Dockerfile
   - Keine Abhängigkeiten von lokalen Node/npm-Installationen außerhalb Docker

4. **Best Practices**
   - Non-root User im Container
   - Minimale Image-Größe
   - Layer-Caching optimieren
   - Security-Scanning (z.B. Trivy)

## Security-Anforderungen

### Authentifizierung & Autorisierung

1. **Authentifizierung**
   - Token-basierte Authentifizierung (JWT empfohlen)
   - Session-Management für Web-UI
   - Secure Password-Handling (falls Passwort-Auth implementiert)
   - Optional: API-Key-Authentifizierung für externe Zugriffe

2. **Autorisierung**
   - Rollenbasierte Zugriffe (falls Multi-User in Zukunft)
   - Read-Only vs. Write-Zugriffe unterscheiden
   - Kritische Operationen (z.B. Force Charge) erfordern explizite Bestätigung

### API-Security

1. **Input-Validierung**
   - Alle API-Inputs validieren (YAML-Parsing, Zahlenbereiche, Strings)
   - Sanitization von User-Inputs
   - Protection gegen Injection-Angriffe (YAML, SQL, etc.)

2. **Rate Limiting**
   - API-Rate-Limiting implementieren
   - Schutz gegen DDoS und Brute-Force-Angriffe

3. **HTTPS/TLS**
   - HTTPS für Production-Deployments (Reverse-Proxy empfohlen)
   - Secure WebSocket-Verbindungen (WSS)

### Container-Security

1. **Docker Security**
   - Non-root User in Containern
   - Minimale Berechtigungen (Principle of Least Privilege)
   - Keine Secrets in Images (Environment-Variablen oder Secrets-Management)
   - Regelmäßige Security-Updates für Base-Images

2. **Network Security**
   - Isolierte Docker-Netzwerke
   - Firewall-Regeln für Container-Kommunikation
   - Keine unnötigen Port-Exposures

### Code-Security

1. **Dependencies**
   - Regelmäßige Updates für bekannte Vulnerabilities
   - Dependency-Scanning (z.B. `npm audit`, `pip-audit`)
   - Keine unsicheren Dependencies

2. **Secrets Management**
   - Keine Hardcoded Secrets
   - Environment-Variablen für sensible Daten
   - Optional: Integration mit Secrets-Management-Tools

## Testing-Anforderungen

### Code Coverage: 90% Minimum

1. **Backend-Tests**
   - Unit-Tests für alle neuen API-Endpunkte
   - Unit-Tests für Konfigurations-Parsing und -Validierung
   - Integration-Tests für API-Integration mit bestehendem Backend
   - Mocking von externen Dependencies (MQTT, Inverter, etc.)

2. **Frontend-Tests**
   - Component-Tests mit React Testing Library
   - Integration-Tests für User-Flows
   - E2E-Tests für kritische Pfade (optional, aber empfohlen)

3. **Test-Infrastruktur**
   - CI/CD-Integration für automatische Test-Ausführung
   - Coverage-Reports in CI/CD-Pipeline
   - Pre-commit Hooks für Test-Ausführung (optional)

4. **Test-Daten**
   - Realistische Test-Daten für alle Szenarien
   - Edge-Cases abdecken
   - Error-Handling testen

### Test-Struktur

```
tests/
├── api/
│   ├── test_config_endpoints.py
│   ├── test_status_endpoints.py
│   └── test_control_endpoints.py
├── frontend/
│   ├── components/
│   ├── hooks/
│   └── utils/
└── integration/
    └── test_ui_backend_integration.py
```

## UI/Wireframe-Anforderungen

### Wireframe-Validierung

1. **Vorhandene Wireframes**
   - `docs/wireframes/batcontrol_dashboard/` - Dashboard-Hauptansicht
   - `docs/wireframes/configuration_editor_1/` - Konfigurations-Editor
   - `docs/wireframes/analytics_stats/` - Historische Daten & Analyse

2. **Wireframe-Compliance**
   - **Alle UI-Implementierungen MÜSSEN exakt mit den Wireframes übereinstimmen**
   - Farben, Typografie, Layout, Komponenten müssen 1:1 umgesetzt werden
   - Responsive Anpassungen müssen dokumentiert sein (siehe `web-ui-briefing.md`)

3. **Design-System**
   - Primary Color: `#13ecec` (Cyan/Türkis)
   - Background Dark: `#112222` / `#102222`
   - Typography: Space Grotesk (Display), Noto Sans (Body)
   - Icons: Material Symbols Outlined
   - Border Radius: 4px (default), 8px (large), 12px (XL), 16px (2XL)

### Workflow für fehlende Wireframes

1. **Wireframe-Anfrage**
   - Wenn für eine neue UI-Komponente kein Wireframe existiert:
     - **SOFORT** Wireframe anfordern
     - Entwicklung **NICHT** ohne Wireframe beginnen
     - Alternative: Briefing-Dokument erstellen und Abnahme einholen

2. **Briefing-Prozess**
   - Erstelle detailliertes Briefing-Dokument (analog zu `web-ui-briefing.md`)
   - Inhalt:
     - Layout-Struktur (Mobile + Desktop)
     - Komponenten-Beschreibung
     - Datenquellen und API-Endpunkte
     - Interaktions-Flows
     - Design-Spezifikationen (Farben, Typografie, etc.)
   - **Abnahme erforderlich** vor Implementierung

3. **Abnahme-Kriterien**
   - Wireframe oder Briefing muss von Product Owner/Designer abgenommen sein
   - Schriftliche Bestätigung der Abnahme
   - Keine Implementierung ohne Abnahme

### Responsive Design

1. **Mobile-First Approach**
   - Basis-Implementierung für Mobile (< 768px)
   - Dann Tablet (768px - 1024px)
   - Dann Desktop (> 1024px)

2. **Desktop-Anpassungen** (siehe `web-ui-briefing.md`)
   - Sidebar-Navigation statt Bottom Navigation
   - Größere Charts und Karten
   - Mehrspaltige Layouts
   - Mehr Details sichtbar

## Technische Stack-Empfehlungen

### Frontend

- **Framework:** React 18+ mit TypeScript
- **Styling:** Tailwind CSS (wie in Wireframes verwendet)
- **Icons:** Material Symbols Outlined
- **Charts:** Recharts oder Chart.js mit react-chartjs-2
- **State Management:** React Context + React Query
- **Build Tool:** Vite (empfohlen) oder Create React App

### Backend-API

- **Framework:** Flask oder FastAPI (Python)
- **API-Standard:** RESTful API
- **Optional:** WebSocket-Support für Echtzeit-Updates
- **Validation:** Pydantic Models (FastAPI) oder Marshmallow (Flask)

### Testing

- **Backend:** pytest, pytest-cov
- **Frontend:** React Testing Library, Jest
- **E2E:** Playwright oder Cypress (optional)

## Implementierungs-Phasen

### Phase 1: MVP Dashboard
- Header mit Status
- Hero SOC Section
- Status Grid (4 Karten)
- Analytics Chart (SOC-Tab)
- Quick Actions (3 Buttons)
- Mobile + Desktop responsive
- **Tests: 90% Coverage**

### Phase 2: Configuration Editor
- Tab-Navigation
- General Settings
- Battery Control (Sliders + Toggles)
- Integrations (EVCC)
- Save-Funktionalität
- YAML-Button (Modal)
- **Tests: 90% Coverage**

### Phase 3: Analytics & Stats
- Zeitraum-Auswahl
- KPI Grid
- Energy Flow Chart
- SOC & Price Chart
- Mode Statistics
- Logs Table
- **Tests: 90% Coverage**

### Phase 4: Erweiterte Features
- Alle Chart-Tabs (Flow, Price)
- Expert Tuning Accordion
- YAML-Raw-Editor
- Export-Funktionen
- Filter & Sortierung
- Real-time Updates (WebSocket)

## Qualitätskriterien

### Performance
- Initial Load: < 2s
- Chart Rendering: < 500ms
- Config Save: < 1s
- Real-time Updates: < 100ms Latency

### Accessibility
- WCAG 2.1 AA Compliance
- Keyboard Navigation
- Screen Reader Support
- High Contrast Mode

### Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 10+)

## Dokumentations-Anforderungen

1. **API-Dokumentation**
   - OpenAPI/Swagger-Spec für alle Endpunkte
   - Request/Response-Beispiele
   - Error-Codes und -Behandlungen

2. **Deployment-Dokumentation**
   - Docker-Setup-Anleitung
   - Environment-Variablen-Dokumentation
   - Reverse-Proxy-Konfiguration (HTTPS)

3. **Entwickler-Dokumentation**
   - Setup-Anleitung für lokale Entwicklung
   - Code-Struktur und Architektur
   - Testing-Anleitung

## Erfolgs-Kriterien

1. ✅ Web-UI vollständig implementiert gemäß Wireframes
2. ✅ Alle Tests bestehen mit 90% Code Coverage
3. ✅ Docker-Container funktioniert in Production
4. ✅ Security-Best-Practices implementiert
5. ✅ API-Dokumentation vollständig
6. ✅ Responsive Design für Mobile und Desktop
7. ✅ Performance-Ziele erreicht
8. ✅ Accessibility-Standards erfüllt

## Wichtige Hinweise

- **Niemals ohne Wireframe oder abgenommenes Briefing entwickeln**
- **Docker ist Pflicht** - keine lokalen Dependencies außerhalb Container
- **90% Code Coverage ist Minimum** - nicht verhandelbar
- **Security first** - alle Security-Anforderungen müssen erfüllt sein
- **Wireframe-Compliance** - exakte Umsetzung der Wireframes ist erforderlich
```

