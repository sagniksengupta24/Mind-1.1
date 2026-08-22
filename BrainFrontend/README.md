# QuoroMind Frontend

Next.js 16 + TypeScript + Tailwind CSS v4 + shadcn/ui + Framer Motion version of the QuoroMind landing page and chat interface.

Connected to the **Brain** backend (Mind1.1) which runs a local Qwen 2.5 Coder 7B model via Ollama.

## Stack

- Next.js 16 App Router
- TypeScript
- Tailwind CSS v4
- shadcn/ui project structure
- Framer Motion

## Prerequisites

- **Ollama** installed and running (`brew install ollama && ollama serve`)
- **Qwen model** pulled (`ollama pull qwen2.5-coder:7b`)
- **Brain backend** running (see Backend Setup below)

## Quick Start

### 1. Backend Setup (Brain)

```bash
cd Brain

# Install Python package (editable)
pip install -e .

# Start the API server
python3 -m mind01.cli serve-api --workspace . --port 8765 --cors-origin http://localhost:3000
```

The backend API will be available at `http://localhost:8765`. Test it:

```bash
curl http://localhost:8765/health
```

### 2. Frontend Setup (BrainFrontend)

```bash
cd BrainFrontend

# Install dependencies
npm install

# Copy and configure environment variables
cp .env.example .env.local
# Edit .env.local if your backend runs on a different port

# Start the dev server
npm run dev
```

Open http://localhost:3000. The chat page is at http://localhost:3000/chat.

### 3. Test the Connection

1. Open http://localhost:3000/chat
2. The topbar should show `Mind v0.9.1 · read-only · Brain` in blue (not "Backend offline")
3. Type a message and press Enter
4. You should see a "Thinking" animation, then the model's response

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MIND_BACKEND_URL` | `http://localhost:8765` | Server-side Brain backend API URL |
| `MIND_API_TOKEN` | _(empty)_ | Server-side API token (must match `MIND_API_TOKEN` on the backend) |

Copy `.env.example` to `.env.local` and adjust as needed. Do NOT use `NEXT_PUBLIC_` prefixes; tokens are kept secure on the Next.js server-side.

## Files

- `app/page.tsx` — landing route
- `app/chat/page.tsx` — chat route
- `app/api/chat/route.ts` — server-side Next.js proxy route for chat
- `app/api/health/route.ts` — server-side Next.js proxy route for health
- `components/landing-page.tsx` — preserved landing UI
- `components/chat-page.tsx` — chat UI with backend model adapter
- `components/ui/button.tsx` — shadcn/ui button component
- `lib/api.ts` — backend API client (health check, chat)
- `lib/utils.ts` — utility functions
- `app/globals.css` — Tailwind v4 entry

## Architecture

To prevent token exposure and secure backend connections, the browser calls relative API routes `/api/chat` and `/api/health` on the Next.js server. The server-side routes proxy requests to the Python backend on port 8765 using server-only environment variables `MIND_BACKEND_URL` and `MIND_API_TOKEN`.

The chat page uses the existing `window.quoroMindModel.generate(messages)` adapter pattern, which points to the relative `/api/chat` endpoint. A health check queries `/api/health` to update the topbar status.

Messages are stored client-side in `localStorage`. Each saved browser conversation is mapped to its own backend `session_id`, so follow-up prompts retain Mind context and switching conversations does not mix sessions.

The proxy fixes chat mode to `read-only`; browser request bodies cannot elevate it. Backend errors retain their HTTP status and structured error payload, including request IDs when supplied by Mind. The UI consumes the v0.9.1 health fields (`workspace_name`, `version`, and `mode`), while the server client is typed for the full chat response (`session_id`, `completion_status`, `output_mode`, `specialist`, and verification metadata).
