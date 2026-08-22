export function Footer() {
  return (
    <>
      <section className="cta-band" id="contact">
        <div className="wrap reveal">
          <h2>
            One mind.<br />
            <span className="grad">It builds the rest.</span>
          </h2>
          <p>Try the model in your browser, or talk to our Bengaluru engineering team about a deployment.</p>
          <a href="/chat" className="btn btn-primary">Try QuoroMind →</a>
        </div>
      </section>

      <footer>
        <div className="wrap">
          <div className="foot-inner">
            <span className="foot-brand">
              Quoro<span style={{ color: 'var(--muted)' }}>Mind</span>
            </span>
            <span className="foot-meta">Designed &amp; built in India · Bengaluru</span>
            <span className="foot-meta">© 2026 QuoroMind AI Pvt. Ltd.</span>
          </div>
        </div>
      </footer>
    </>
  );
}
