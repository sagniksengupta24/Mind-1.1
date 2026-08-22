import { NextResponse } from 'next/server';
import { BackendApiError, checkHealth } from '@/lib/api';

export async function GET() {
  try {
    const data = await checkHealth();
    return NextResponse.json(data);
  } catch (error: unknown) {
    if (error instanceof BackendApiError) {
      return NextResponse.json(
        error.payload || { error: { message: error.message } },
        { status: error.status },
      );
    }
    const message = error instanceof Error ? error.message : 'Internal Server Error';
    return NextResponse.json({ error: { message } }, { status: 500 });
  }
}
