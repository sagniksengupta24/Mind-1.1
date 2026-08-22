# Semiconductor Notes

Put VLSI, Verilog, SystemVerilog, EDA, FPGA, timing, and semiconductor notes in
this folder, then run:

```bash
python3 -m mind01.cli index-docs docs --workspace .
python3 -m mind01.cli index-docs docs --workspace . --embed --embedding-model nomic-embed-text
```

The default path uses SQLite keyword search. Add `--embed` after pulling an
Ollama embedding model such as `nomic-embed-text` to store local semantic
vectors for hybrid retrieval.

## Timing: Setup Time

Setup time is the minimum time that input data must stay stable before the
active clock edge reaches a flip-flop. If data changes too close to the clock
edge, the flip-flop can capture the wrong value or become metastable.

In STA, a setup check compares the latest data arrival time against the capture
clock edge minus setup requirement, clock uncertainty, and other timing margins.
A practical fix for a setup violation is to reduce combinational delay, improve
placement, add pipelining, or adjust the clocking architecture.
