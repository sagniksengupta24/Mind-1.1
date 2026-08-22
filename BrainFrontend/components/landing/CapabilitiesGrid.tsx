export function CapabilitiesGrid() {
  return (
    <section className="section" id="capabilities">
      <div className="wrap">
        <div className="section-head reveal">
          <span className="eyebrow">The runtime</span>
          <h2>Deterministic RTL engineering and verification.</h2>
          <p>
            Mind1.1 bridges language models with EDA tools — generating synthesizable Verilog, writing testbenches, and verifying functional correctness via deterministic simulation loops.
          </p>
        </div>
        <div className="caps">
          <div className="cap reveal" style={{ background: "rgba(43,80,224,0.03)" }}>
            <div className="cap-ic">
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="4" />
                <path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1" />
              </svg>
            </div>
            <h3>Open-Weight Intelligence</h3>
            <p>
              Optimized for 30–50B parameter open-weight models with long context windows — capable of analyzing entire HDL modules, register definitions, and protocol specifications.
            </p>
          </div>
          <div className="cap reveal">
            <div className="cap-ic">
              <svg viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="1" />
                <circle cx="12" cy="12" r="2.5" />
                <path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3" />
              </svg>
            </div>
            <h3>Simulator in the Loop</h3>
            <p>
              Integrated with Icarus Verilog and EDA toolchains. Every generated module is compiled and verified against testbench assertions inside a secure sandbox.
            </p>
          </div>
          <div className="cap reveal">
            <div className="cap-ic">
              <svg viewBox="0 0 24 24">
                <path d="M3 12a9 9 0 0 1 9-9M21 12a9 9 0 0 1-9 9" />
                <path d="M12 3l3 3-3 3M12 21l-3-3 3-3" />
              </svg>
            </div>
            <h3>Cryptographic Receipts</h3>
            <p>
              Every file mutation, test run, and evidence check generates a hash-chained receipt with automated rollback capability if post-write verification fails.
            </p>
          </div>
          <div className="cap reveal">
            <div className="cap-ic">
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="3" />
                <path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M19.1 4.9l-2.8 2.8M7.7 16.3l-2.8 2.8" />
              </svg>
            </div>
            <h3>Local-First Sovereign AI</h3>
            <p>
              Self-hosted on your own workstation or private infrastructure with zero external telemetry, strict secret redaction, and total data sovereignty.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
