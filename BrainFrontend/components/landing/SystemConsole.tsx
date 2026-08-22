'use client';

import { useEffect, useState } from 'react';
import { SafeConsoleVisual } from './SafeConsoleVisual';

function FallbackSVG() {
  return (
    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[200px]">
      <path className="trace" d="M200 200 L200 74"/>
      <path className="trace" d="M200 200 L326 262"/>
      <path className="trace" d="M200 200 L74 262"/>
      <circle className="node-core" cx="200" cy="200" r="46"/>
      <text className="sig-core-lbl" x="200" y="204" textAnchor="middle">Quoro</text>
      <text className="sig-core-lbl" x="200" y="218" textAnchor="middle">Mind</text>
    </svg>
  );
}

export function SystemConsole() {
  const [logs, setLogs] = useState<string[]>([
    "INIT Mind1.1 RTL engineering agent runtime...",
    "Loaded Verilog/SystemVerilog verification suite.",
    "Sandboxed simulator executor: OK",
    "CompletionAuthority policy: active",
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setLogs(prev => {
        const newLogs = [...prev, `[${new Date().toISOString().split('T')[1].slice(0, 8)}] System check OK. \u0394t = ${Math.random().toFixed(4)}`];
        if (newLogs.length > 10) newLogs.shift();
        return newLogs;
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="system-console" aria-hidden="true">
      <div className="sc-head">
        <div className="sc-dots">
          <span />
          <span />
          <span />
        </div>
        <div className="sc-tab">Telemetry Node</div>
      </div>
      <div className="sc-body">
        <div className="sc-logs">
          {logs.map((log, i) => (
            <div key={i} className="sc-log-line">
              {log.includes('LIFT') || log.includes('INIT') ? <span>{log}</span> : log}
            </div>
          ))}
        </div>
        <div className="sc-visual">
          <div className="absolute inset-0 flex items-center justify-center">
            {/* 3D element with safety pre-flight & error boundary */}
            <div style={{ width: '100%', height: '100%', maxWidth: '200px', maxHeight: '200px' }}>
              <SafeConsoleVisual fallback={<FallbackSVG />} />
            </div>
          </div>
          {/* Decorative nodes */}
          <div className="console-graph">
            <div className="graph-node" style={{ top: '20%', left: '20%' }} />
            <div className="graph-node" style={{ top: '70%', left: '80%' }} />
            <div className="graph-line" style={{ top: '22%', left: '22%', width: '100px', transform: 'rotate(45deg)' }} />
          </div>
        </div>
      </div>
    </div>
  );
}
