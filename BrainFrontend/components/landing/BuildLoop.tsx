export function BuildLoop() {
  return (
    <>
      <section className="section" id="process">
        <div className="wrap">
          <div className="loop reveal">
            <div className="section-head">
              <span className="eyebrow" style={{ color: 'var(--cobalt-soft)' }}>
                The agent loop
              </span>
              <h2>Plan. Generate. Simulate. Verify.</h2>
              <p>
                A closed-loop verification pipeline connecting open-weight LLMs with EDA simulators and deterministic evidence authorities.
              </p>
            </div>
            <div className="loop-steps">
              <div className="step">
                <div className="n">01</div>
                <h4>Plan</h4>
                <p>Parses engineering specs into verifiable hardware architecture and timing constraints.</p>
              </div>
              <div className="step">
                <div className="n">02</div>
                <h4>Generate</h4>
                <p>Synthesizes clean Verilog/SystemVerilog modules and self-checking testbenches.</p>
              </div>
              <div className="step">
                <div className="n">03</div>
                <h4>Simulate</h4>
                <p>Runs sandboxed compilation and waveform simulation with Icarus Verilog.</p>
              </div>
              <div className="step">
                <div className="n">04</div>
                <h4>Verify</h4>
                <p>CompletionAuthority validates testbench assertion receipts before accepting code.</p>
              </div>
              <div className="step">
                <div className="n">05</div>
                <h4>Commit</h4>
                <p>Records cryptographic audit receipts with automated state rollback safety.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="section" style={{ paddingTop: 0 }}>
        <div className="wrap">
          <div className="stats">
            <div className="stat reveal">
              <div className="v" data-to="70"><em>0</em>B</div>
              <div className="l">Parameters</div>
            </div>
            <div className="stat reveal">
              <div className="v" data-to="256"><em>0</em>K</div>
              <div className="l">Context window</div>
            </div>
            <div className="stat reveal">
              <div className="v" data-to="40"><em>0</em>ms</div>
              <div className="l">First-token latency</div>
            </div>
            <div className="stat reveal">
              <div className="v"><em>100</em>%</div>
              <div className="l">Built in India</div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
