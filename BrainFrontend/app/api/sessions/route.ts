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

export async function GET() {
  try {
    const upstream = await fetch(`${BACKEND_URL}/sessions`, {
      headers: apiHeaders(),
      cache: 'no-store',
    });
    if (!upstream.ok) {
      throw new BackendApiError(upstream.status, null);
    }
    const data = await upstream.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    return errorResponse(error);
  }
}

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
    const upstream = await fetch(`${BACKEND_URL}/sessions`, {
      method: 'POST',
      headers: apiHeaders(),
      body: JSON.stringify(body),
      cache: 'no-store',
    });
    if (!upstream.ok) {
      throw new BackendApiError(upstream.status, null);
    }
    const data = await upstream.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    return errorResponse(error);
  }
}
