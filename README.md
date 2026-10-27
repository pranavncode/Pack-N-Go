# AI Travel Intelligence Platform

An AI-powered travel planning platform that helps travellers discover destinations, evaluate trip conditions, plan itineraries, estimate costs, and prepare personalized packing lists.

> **Project status:** Early development — backend foundation and initial weather integration are being implemented. Features described as planned are not yet complete.

## Vision

The platform aims to help users answer:

- Where should I travel to get the experience I want?
- Is my chosen destination suitable for my dates and activities?
- What should I pack for this specific trip?
- How can I plan a practical itinerary within my budget?
- What recent destination information and safety considerations should I know?

The initial release is a website. The backend is being designed so that a future React Native application can use the same APIs.

## Planned MVP Features

- Trip request validation and persistence
- Destination discovery based on user preferences
- Weather retrieval and suitability assessment
- Personalized packing checklist
- Day-wise itinerary generation
- Budget estimation
- Basic route and transport information
- Recent destination observations from accessible social and travel-community sources
- Safety considerations and source references

## Technology Stack

| Area | Technology | Current role |
|---|---|---|
| Web frontend | React, TypeScript, Vite | Planned |
| Backend | Python, Django, Django REST Framework | In development |
| Database | PostgreSQL | Intended primary database; SQLite may be used temporarily |
| Validation | DRF serializers, Pydantic | Request validation and normalized integration schemas |
| HTTP client | HTTPX | External API requests |
| Weather data | Open-Meteo Forecast API | Initial weather provider |
| Caching | Django cache framework | Weather response caching |
| Future mobile client | React Native | Planned; will reuse backend APIs |
| AI/LLM | Provider to be configured | Planned for preference extraction and explanations |
| Places, routing, social sources | Providers to be selected and validated | Planned |

## Repository Structure

The current backend structure is expected to grow into:

```text
travel-intelligence/
├── frontend/                 # React + TypeScript + Vite (planned)
├── backend/
│   ├── config/               # Django project settings and root URLs
│   ├── trips/                # Trip models and trip APIs
│   ├── weather/              # Weather API integration
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                  # Local secrets; never commit
├── docs/                     # Architecture and API notes (planned)
├── .gitignore
└── README.md
```

Some directories may not exist until their implementation milestone begins.

## Getting Started — Backend

### Prerequisites

- Python 3.10+ (use a version supported by the Django version installed)
- Git
- PostgreSQL, if using PostgreSQL rather than temporary SQLite
- An internet connection for the weather integration

### 1. Clone or open the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd travel-intelligence
```

If you already have the project locally, open its root directory instead.

### 2. Create and activate a virtual environment

```bash
cd backend
python -m venv venv
```

**Windows PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD**

```bat
venv\Scripts\activate.bat
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 3. Install backend dependencies

If `requirements.txt` exists and is up to date:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The project setup so far has used these packages:

```bash
pip install django djangorestframework django-cors-headers python-dotenv "psycopg[binary]" pydantic httpx
```

After installing dependencies, update the requirements file when appropriate:

```bash
pip freeze > requirements.txt
```

### 4. Configure environment variables

Create `backend/.env`:

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=travel_intelligence
DB_USER=postgres
DB_PASSWORD=your_local_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Create the PostgreSQL database named `travel_intelligence` before running migrations if PostgreSQL is configured in Django.

If the project is temporarily using Django's default SQLite configuration, PostgreSQL variables are not required until the database configuration is switched.

**Security:** Do not commit `.env`, API keys, database passwords, or production secrets. Keep `DJANGO_DEBUG=False` in production and use a properly managed secret.

### 5. Run checks and migrations

From the `backend/` directory:

```bash
python manage.py check
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The backend should be available at:

```text
http://127.0.0.1:8000/
```

## API Endpoints Implemented or In Progress

These endpoints reflect the current development plan. Verify the corresponding URL configuration before relying on an endpoint.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/trips/` | Create and persist a validated trip |
| `GET` | `/api/v1/trips/<id>/` | Retrieve a saved trip |
| `POST` | `/api/v1/weather/assess/` | Request normalized weather data for coordinates and dates |

### Create a trip

Send a `POST` request to `http://127.0.0.1:8000/api/v1/trips/` with `Content-Type: application/json`:

```json
{
  "mode": "discover",
  "origin": "Dehradun, India",
  "destination": "",
  "start_date": "2026-12-10",
  "end_date": "2026-12-13",
  "travellers": 2,
  "budget": "8000.00",
  "currency": "INR",
  "preferences": {
    "snow": 0.9,
    "trekking": 0.8,
    "peaceful": 0.9
  },
  "transport": {
    "personal_vehicle": false
  },
  "must_visit": [],
  "constraints": {
    "pace": "balanced"
  }
}
```

A successful create request should return `201 Created` and include the saved trip ID.

### Request weather data

Send a `POST` request to `http://127.0.0.1:8000/api/v1/weather/assess/`:

```json
{
  "latitude": 30.123,
  "longitude": 79.456,
  "start_date": "2026-10-28",
  "end_date": "2026-11-02"
}
```

Use coordinates for the destination being tested. The weather adapter requests supported daily forecast variables from Open-Meteo and maps the response to an internal schema. Forecast availability depends on the requested dates and provider capabilities.

The weather adapter currently uses a short-lived cache. Persistent weather snapshots and trip-linked weather assessments are future improvements.

## Testing

Run backend tests from `backend/`:

```bash
python manage.py test
```

Run checks:

```bash
python manage.py check
```

External API integrations should be tested with mocked responses as well as controlled live requests. Tests should not depend on an external service being available.

## Architecture Principles

1. **One backend, multiple clients:** the website and future mobile app will use the same versioned REST API.
2. **Evidence before generation:** retrieve real data before generating travel recommendations.
3. **Normalized data:** external providers should be mapped to internal schemas.
4. **Transparent uncertainty:** missing, stale, or unverified information must not be presented as fact.
5. **Deterministic validation:** dates, budgets, itinerary feasibility, and critical restrictions should be checked in code.
6. **Provider abstraction:** keep weather, places, routing, social, and LLM integrations replaceable.
7. **Privacy and security:** protect credentials and collect only the user data required for the feature.

## Development Roadmap

- [x] Initial Django project and trip API design
- [x] Initial trip persistence design
- [ ] Verify trip model, migrations, endpoints, and automated tests locally
- [ ] Complete and test weather adapter, validation, caching, and error handling
- [ ] Link weather assessments to saved trips
- [ ] Add destination catalogue and place retrieval
- [ ] Build destination matching and feasibility rules
- [ ] Build the packing recommendation engine
- [ ] Add itinerary and budget engines
- [ ] Add permitted social/travel-content retrieval with source timestamps
- [ ] Build React frontend and connect it to the API
- [ ] Evaluate recommendation quality against test scenarios
- [ ] Prepare deployment and production security configuration

Checkboxes indicate project planning status and should be updated as implementation is verified.

## Current Limitations

- This is an early-stage project; the complete AI travel-planning workflow is not yet implemented.
- Destination discovery, itinerary generation, budget optimization, and packing recommendations are planned features.
- Social media access depends on each platform's API, permissions, quotas, and terms; unrestricted scraping is not assumed.
- Weather forecasts do not guarantee future conditions, and distant dates may not have forecast coverage.
- Accommodation prices and availability must come from a suitable provider before being shown as current.
- The initial weather endpoint accepts coordinates; destination-name resolution is a separate planned capability.
- Production authentication, rate limiting, monitoring, deployment, and user-data controls still need to be implemented and reviewed.

## Contributing / Development Notes

- Keep secrets in environment variables.
- Add tests for new serializers, services, API endpoints, and failure cases.
- Keep provider-specific code inside `integrations/` or dedicated service adapters as the project grows.
- Update API documentation and this README when endpoints or setup instructions change.
- Do not mark a feature complete until it has been tested locally.

## License

No license has been selected yet. Add a `LICENSE` file before distributing or accepting external contributions.
