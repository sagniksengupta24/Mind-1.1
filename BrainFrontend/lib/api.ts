/**
 * Mind1.1 Backend API Client
 *
 * Connects the QuoroMind frontend to the Brain backend API.
 * All configuration is driven by environment variables.
 */

export const BACKEND_URL =
  (typeof process !== 'undefined' && process.env?.MIND_BACKEND_URL) ||
  'http://localhost:8765';

const API_TOKEN =
  (typeof process !== 'undefined' && process.env?.MIND_API_TOKEN) || '';

/* ── Types ── */

export interface HealthResponse {
  ok: boolean;
  workspace_name: string;
  version: string;
  mode: string;
  default_mode: string;
  auth_enabled: boolean;
  dirty_state_count: number;
  receipt_chain_head_present: boolean;
  trace_chain_head_present: boolean;
}

export interface ChatResponse {
  session_id: string;
  text: string;
  steps: number;
  trace: string[];
  specialist: string | null;
  verification: Record<string, unknown> | null;
  parser_incidents: Array<Record<string, unknown>>;
  completion_status: string;
  output_mode: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details: Record<string, unknown>;
    request_id: string;
    trace_id: string | null;
  };
}

export class BackendApiError extends Error {
  readonly status: number;
  readonly payload: ApiError | null;

  constructor(status: number, payload: ApiError | null) {
    super(payload?.error?.message || `Backend error (${status})`);
    this.name = 'BackendApiError';
    this.status = status;
    this.payload = payload;
  }
}

/* ── Helpers ── */

export function headers(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  if (API_TOKEN) {
    h['X-Mind-Token'] = API_TOKEN;
  }
  return h;
}

export function apiHeaders(): Record<string, string> {
  return headers();
}

/**
 * Extract a user-friendly error message from a backend response or network error.
 */
async function backendError(res: Response): Promise<BackendApiError> {
  try {
    const body = (await res.json()) as ApiError;
    return new BackendApiError(res.status, body);
  } catch {
    return new BackendApiError(res.status, null);
  }
}

/* ── Public API ── */

/**
 * Check backend health. Returns the health payload or throws.
 */
export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${BACKEND_URL}/health`, {
    headers: headers(),
    cache: 'no-store',
  });
  if (!res.ok) {
    throw await backendError(res);
  }
  return res.json() as Promise<HealthResponse>;
}

/**
 * Stream a chat prompt over SSE. Emits one callback per SSE frame (lifecycle
 * stages and tool call/result events) and resolves with the final `done`
 * payload. Falls back to a single non-streaming JSON call when the backend
 * answers with plain JSON (backward compatibility).
 */
export async function streamChat(
  prompt: string,
  sessionId: string | undefined,
  onEvent: (event: string, data: Record<string, unknown>) => void,
): Promise<ChatResponse> {
  const body: Record<string, unknown> = {
    prompt,
    mode: 'read-only',
    trace: false,
    stream: true,
  };
  if (sessionId) {
    body.session_id = sessionId;
  }

  const res = await fetch(`${BACKEND_URL}/chat`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw await backendError(res);
  }

  const contentType = res.headers.get('content-type') || '';
  if (!contentType.includes('text/event-stream')) {
    // Backend answered JSON (older or non-streaming path): single result.
    return res.json() as Promise<ChatResponse>;
  }

  if (!res.body) {
    throw new Error('Streaming response has no body.');
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let done: ChatResponse | null = null;

  const emitFrame = (frame: string) => {
    let event = 'message';
    let dataLine: string | null = null;
    for (const line of frame.split('\n')) {
      if (line.startsWith('event: ')) event = line.slice(7).trim();
      else if (line.startsWith('data: ')) dataLine = line.slice(6);
    }
    if (dataLine === null) return;
    let data: Record<string, unknown> = {};
    try {
      data = JSON.parse(dataLine) as Record<string, unknown>;
    } catch {
      return;
    }
    if (event === 'done') {
      done = data as unknown as ChatResponse;
    } else {
      onEvent(event, data);
    }
  };

  for (;;) {
    const { value, done: readerDone } = await reader.read();
    if (readerDone) break;
    buffer += decoder.decode(value, { stream: true });
    let boundary = buffer.indexOf('\n\n');
    while (boundary >= 0) {
      const frame = buffer.slice(0, boundary).trim();
      buffer = buffer.slice(boundary + 2);
      if (frame) emitFrame(frame);
      boundary = buffer.indexOf('\n\n');
    }
  }

  if (done) return done;
  // Stream ended without a done frame (e.g. backend error event).
  throw new Error('Stream ended without a final response.');
}

/**
 * Send a chat prompt to the backend Qwen model and return the response.
 */
export async function sendChat(
  prompt: string,
  sessionId?: string,
): Promise<ChatResponse> {
  const body: Record<string, unknown> = {
    prompt,
    mode: 'read-only',
    trace: false,
  };
  if (sessionId) {
    body.session_id = sessionId;
  }

  const res = await fetch(`${BACKEND_URL}/chat`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw await backendError(res);
  }
  return res.json() as Promise<ChatResponse>;
}
