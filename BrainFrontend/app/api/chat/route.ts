import { NextResponse } from 'next/server';
import { BackendApiError, BACKEND_URL, apiHeaders } from '@/lib/api';

function errorResponse(error: unknown) {
  if (error instanceof BackendApiError) {
    return NextResponse.json(
      error.payload || { error: { message: error.message } },
      { status: error.status },
    );
  }
  const message = error instanceof Error ? error.message : 'Internal Server Error';
  return NextResponse.json({ error: { message } }, { status: 500 });
}

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as Record<string, unknown>;
    const { prompt, session_id, stream } = body;
    if (typeof prompt !== 'string' || !prompt.trim()) {
      return NextResponse.json(
        { error: { message: 'Prompt is required' } },
        { status: 400 }
      );
    }
    if (session_id !== undefined && typeof session_id !== 'string') {
      return NextResponse.json(
        { error: { message: 'session_id must be a string' } },
        { status: 400 },
      );
    }
    const payload: Record<string, unknown> = {
      prompt: prompt.trim(),
      mode: 'read-only',
      trace: false,
    };
    if (session_id) payload.session_id = session_id;
    if (stream === true) payload.stream = true;

    const upstream = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: apiHeaders(),
      body: JSON.stringify(payload),
      cache: 'no-store',
    });

    if (!upstream.ok) {
      // Non-streaming error: preserve the backend's structured error body.
      let errPayload: unknown = null;
      try {
        errPayload = await upstream.json();
      } catch {
        errPayload = null;
      }
      throw new BackendApiError(upstream.status, errPayload as never);
    }

    const contentType = upstream.headers.get('content-type') || '';
    if (contentType.includes('text/event-stream')) {
      // Streaming passthrough: relay the SSE body verbatim so the browser
      // receives the same event frames the backend emitted.
      return new Response(upstream.body, {
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream; charset=utf-8',
          'Cache-Control': 'no-cache',
          Connection: 'keep-alive',
          'X-Accel-Buffering': 'no',
        },
      });
    }

    // Non-streaming response: return the JSON payload as before.
    const data = await upstream.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    return errorResponse(error);
  }
}
