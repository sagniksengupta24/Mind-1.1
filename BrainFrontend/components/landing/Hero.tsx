import Link from 'next/link';
import { SystemConsole } from './SystemConsole';

export function Hero() {
  return (
    <section className="hero">
      <div className="hero-halo"></div>
      <div className="wrap">
        <div className="hero-grid">
          <div>
            <div className="hero-eyebrow eyebrow">
              <span className="dot"></span> Verification-First AI Runtime · Bengaluru, India
            </div>
            <h1>
              Local-First AI.<br />
              <span className="grad">Deterministic RTL Verification.</span>
            </h1>
            <p className="hero-sub">
              Mind1.1 is an engineering-agent runtime built for semiconductor design, synthesizable Verilog generation, and simulation loops — powered by open-weight models.
            </p>
            <div className="hero-actions">
              <Link href="/chat" className="btn btn-primary">
                Open Mind1.1 Studio →
              </Link>
              <a href="#process" className="btn btn-ghost">
                Architecture & Verification
              </a>
            </div>
            <div className="hero-meta">
              <div className="m">
                <span className="mv">Verilog / SV</span>
                <span className="ml">RTL Engineering</span>
              </div>
              <div className="m">
                <span className="mv">100% Verified</span>
                <span className="ml">Simulation in-the-loop</span>
              </div>
              <div className="m">
                <span className="mv">Local-First</span>
                <span className="ml">Self-Hosted Runtime</span>
              </div>
            </div>
          </div>

          <div className="hero-visual" style={{ maxWidth: 440, margin: '0 auto', width: '100%' }}>
            <SystemConsole />
          </div>
        </div>
      </div>
    </section>
  );
}
