# Universal Scoring Rubric

Each prompt in the Mind1.1 benchmark suite is evaluated on a scale of 0 to 5 across six distinct categories.

## Scoring Categories and Weightings

```
                                 Total Score
                                      |
         +----------+----------+------+------+----------+----------+
         |          |          |             |          |          |
         v          v          v             v          v          v
     [Parser]    [Task]     [Tool]      [Verify]     [No-Hal]   [Final]
       20%        25%        20%           15%         10%        10%
```

The final weighted score is calculated using the following formula:

$$\text{Total Score} = (P \times 0.20) + (T \times 0.25) + (U \times 0.20) + (V \times 0.15) + (H \times 0.10) + (Q \times 0.10)$$

Where:
* $P$ = Parser compliance (weight: 20%)
* $T$ = Task correctness (weight: 25%)
* $U$ = Tool-use correctness (weight: 20%)
* $V$ = Verification behavior (weight: 15%)
* $H$ = Hallucination control (weight: 10%)
* $Q$ = Final answer quality (weight: 10%)

---

## Evaluation Criteria

### 1. Parser Compliance (P)
Measures adherence to the canonical versioned JSON tool-call/final schema and current response mode.
* **5**: Outputs exactly one block with correct structure and zero trailing text or markdown fence wrappers.
* **3**: One valid object required safe structural extraction and was recorded as a parser incident.
* **1**: Mixes formats, uses markdown code fences (` ```json `) around tags, or writes explanations outside blocks.
* **0**: Outputs malformed, multiple, contradictory, hidden-tool, or wrong-mode objects.

### 2. Task Correctness (T)
Measures the technical accuracy of the final answer (code correctness, synthesizable RTL compliance, mathematical derivations, language translations).
* **5**: 100% correct, meets all constraints, synthesizable hardware structures, mathematically verified, correct code.
* **3**: Partially correct logic, but contains minor logic edge case failures or missing constraints.
* **1**: Highly flawed solution, introduces major compiler errors, timing violations, or incorrect logic values.
* **0**: Completely incorrect, refuses to solve valid tasks, or generates garbage output.

### 3. Tool-Use Correctness (U)
Measures the selection and execution sequence of active tool calls.
* **5**: Uses `project_map` or `list_files` before reading files. Calls tools sequentially and accurately. Matches schemas.
* **3**: Calls correct tools but skips structural mapping exploration steps.
* **1**: Calls incorrect tool names, missing arguments, or invalid parameter types.
* **0**: Attempts direct modifications without reading files first, or loops identical failing parameters.

### 4. Verification Behavior (V)
Measures validation checks run by the agent before completing tasks.
* **5**: Runs unit tests (`pytest`, `npm test`) using allowed commands, compiles code via compile modules, or runs python check scripts.
* **3**: Claims verification succeeded without running tool validation commands.
* **1**: Ignores test failures and submits compilation errors as successful.
* **0**: Fails to run any checks or verify logic boundaries.

### 5. Hallucination Control (H)
Measures the accuracy of file paths, functions, and data references.
* **5**: Only references verified workspace files. Zero imaginary paths or functions.
* **3**: Mentions typical files from memory that exist but does not verify them.
* **1**: References nonexistent paths, libraries, or APIs.
* **0**: Hallucinates file content or invents APIs to bypass requirements.

### 6. Final Answer Quality (Q)
Measures readability, formatting, language alignment, and conciseness.
* **5**: Concise technical details, correct bilingual language styles (Hinglish/Bengali), structured math variables.
* **3**: Provides correct information but is verbose or contains awkward local translations.
* **1**: Hard to read, uses raw console dumps, or fails technical language rules.
* **0**: Incoherent or blank output.
