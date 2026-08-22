'use client';

import { Component, ReactNode, ErrorInfo, useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import dynamic from 'next/dynamic';
import Flourish3D from './Flourish3D';

/**
 * True pre-flight check. Creates a throwaway 2D-less <canvas> and tries to get
 * a WebGL context WITHOUT going through three.js. If this fails, we never even
 * attempt to mount <Canvas>, which is what stops the repeated console spam and
 * the unhandled rejection — three.js's retry-with-fallback-attributes behavior
 * never runs because we never call it.
 */
function supportsWebGL(): boolean {
  if (typeof window === 'undefined') return false;
  try {
    const canvas = document.createElement('canvas');
    const gl =
      canvas.getContext('webgl2', { failIfMajorPerformanceCaveat: false }) ||
      canvas.getContext('webgl', { failIfMajorPerformanceCaveat: false }) ||
      canvas.getContext('experimental-webgl', { failIfMajorPerformanceCaveat: false });
    const ok = !!gl;
    // release the context immediately, we don't need it
    canvas.width = 0;
    canvas.height = 0;
    return ok;
  } catch {
    return false;
  }
}

/**
 * Second layer of defense. If something inside the Canvas tree still throws
 * after the pre-flight check passed (driver quirks, context lost mid-session),
 * this catches it and swaps to the static fallback instead of crashing the page.
 */
class WebGLErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode; fallback: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  componentDidCatch(error: Error, info: ErrorInfo) {
    // Log quietly — this is an expected, handled fallback path, not a bug report.
    console.warn('[SystemConsole] 3D context unavailable, using static fallback.', error.message);
  }
  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}

function ConsoleCanvas({ reducedMotion }: { reducedMotion: boolean }) {
  return (
    <Canvas
      dpr={[1, 1.5]}
      camera={{ position: [0, 0, 5], fov: 45 }}
      frameloop={reducedMotion ? 'demand' : 'always'}
      gl={{
        antialias: true,
        alpha: true,
        // 'default' lets the browser hand back a software-rendered context
        // instead of refusing outright the way 'high-performance' can on
        // GPU-less sandboxes.
        powerPreference: 'default',
        failIfMajorPerformanceCaveat: false,
      }}
      onCreated={({ gl }) => {
        gl.setClearColor(0x000000, 0);
      }}
    >
      <Flourish3D reducedMotion={reducedMotion} />
    </Canvas>
  );
}

/**
 * Public component. Use this in the hero / SystemConsole — never import
 * <Canvas> directly elsewhere.
 */
function SafeConsoleVisualInner({ fallback }: { fallback: ReactNode }) {
  const [canRender3D, setCanRender3D] = useState<boolean | null>(null);
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    setCanRender3D(supportsWebGL());
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mq.matches);
    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  // Render nothing (or a skeleton) until the check resolves, to avoid a flash
  // of the 3D component immediately followed by a fallback swap.
  if (canRender3D === null) {
    return <div className="console-visual-placeholder" aria-hidden="true" />;
  }

  if (!canRender3D) {
    return <>{fallback}</>;
  }

  return (
    <WebGLErrorBoundary fallback={fallback}>
      <ConsoleCanvas reducedMotion={reducedMotion} />
    </WebGLErrorBoundary>
  );
}

// ssr: false is required — supportsWebGL() and Canvas both need `window`.
export const SafeConsoleVisual = dynamic(
  () => Promise.resolve(SafeConsoleVisualInner),
  { ssr: false }
);
