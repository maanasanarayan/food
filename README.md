# Indian Food Companion

AI-powered Indian vegetarian food recommendation chat app with personalized dietary preferences, allergen-safe filtering, and streaming responses.

## Quick Start

```bash
# Clone and enter the repo
git clone <repo-url> && cd food

# Set your OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# One-command setup
./setup.sh
```

Open <http://localhost:5173> and start chatting.

---

## Architecture

```mermaid
graph TB
    subgraph Client
        UI["React + shadcn/ui"]
    end
    
    subgraph Docker["Docker Compose"]
        subgraph Frontend
            NGINX["NGINX :5173"]
        end
        
        subgraph Backend
            API["FastAPI :8080"]
            MCP["MCP Server"]
        end
        
        subgraph Storage
            PG[("PostgreSQL :5432")]
            CHROMA[("ChromaDB :8001")]
        end
    end
    
    subgraph External
        OPENAI["OpenAI API"]
    end
    
    UI --> NGINX
    NGINX --> API
    API --> MCP
    API --> PG
    API --> CHROMA
    API --> OPENAI
```

## Components

```mermaid
graph LR
    subgraph FE["Frontend"]
        App["App.tsx"]
        Chat["ChatMessage"]
        Composer["ChatComposer"]
        Prefs["PreferencesDialog"]
    end
    
    subgraph BE["Backend"]
        ChatAPI["Chat API"]
        PrefsAPI["Preferences API"]
        AdminAPI["Admin API"]
    end
    
    subgraph RAG["RAG Pipeline"]
        Retriever["Retriever"]
        LLM["OpenAI Client"]
    end
    
    App --> Chat
    App --> Composer
    App --> Prefs
    Composer --> ChatAPI
    ChatAPI --> Retriever
    ChatAPI --> LLM
    Prefs --> PrefsAPI
```

---

## Tech Stack

| Layer | Technology | Version |
| ----- | ---------- | ------- |
| Frontend | React + Vite | 19.x + 7.x |
| UI | shadcn/ui + Tailwind | 3.7 + 4.x |
| Package Manager | Bun | 1.3+ |
| Backend | FastAPI | 0.128+ |
| Python Deps | uv | latest |
| Vector DB | ChromaDB | 1.4+ |
| Database | PostgreSQL | 17 |
| LLM | OpenAI | gpt-4o-mini |
| Tools | MCP Python SDK | 1.25+ |

---

## Project Structure

```text
food/
├── setup.sh               # One-command bootstrap
├── docker-compose.yml     # All services
├── .env.example           # Environment template
├── backend/
│   ├── pyproject.toml     # uv dependencies
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py        # FastAPI app
│   │   ├── api/           # API endpoints
│   │   ├── db/            # SQLModel models
│   │   ├── rag/           # ChromaDB retriever
│   │   ├── llm/           # OpenAI client
│   │   └── mcp/           # MCP tools server
│   └── data/
│       └── foods.json     # 57 Indian dishes
└── frontend/
    ├── package.json       # Bun dependencies
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── App.tsx
        ├── components/    # Chat UI components
        ├── hooks/         # useChat hook
        └── lib/           # API client
```

---

## Development

### Local Development (without Docker)

**Backend:**

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8080
```

**Frontend:**

```bash
cd frontend
bun install
bun run dev
```

**Services (Postgres + ChromaDB):**

```bash
docker compose up postgres chroma -d
```

### Seed Data

```bash
curl -X POST http://localhost:8080/api/admin/ingest
```

### API Docs

Visit <http://localhost:8080/docs> for interactive Swagger UI.

---

## Features

### Personalized Recommendations

- Dietary preferences (spice level, cuisine types)
- Allergen exclusion (dairy, gluten, nuts, etc.)
- Health goals (high protein, low carb, etc.)

### Streaming Chat

- Real-time SSE streaming responses
- Quick prompt chips for common queries
- Preference persistence via localStorage

### Comprehensive Food Database

- 57 authentic Indian vegetarian dishes
- South Indian, North Indian, Gujarati, Bengali, Rajasthani, Maharashtrian cuisines
- Nutrition data, prep times, spice levels

### MCP Tools

- `search_food` - Semantic search with filtering
- `get_food_details` - Get full food info
- `save_preferences` - Update user prefs

---

## API Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | `/api/chat` | SSE streaming chat |
| GET | `/api/preferences/{user_id}` | Get preferences |
| PUT | `/api/preferences/{user_id}` | Update preferences |
| GET | `/api/conversations/{user_id}` | List conversations |
| POST | `/api/admin/ingest` | Seed food data |
| GET | `/api/admin/stats` | DB statistics |

---

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `OPENAI_API_KEY` | OpenAI API key | (required) |
| `DATABASE_URL` | Postgres connection | `postgresql://food:food@postgres:5432/food` |
| `CHROMA_HOST` | ChromaDB host | `chroma` |
| `CHROMA_PORT` | ChromaDB port | `8000` |

---

## Cleanup

```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

---

## License

MIT
