# MASTER PLAN 00 — Typed Agent Contracts
**Feature:** JSON Schema validation layer for all agent outputs
**Priority:** CRITICAL — foundational for every other plan
**Estimated effort:** 3–4 days
**Depends on:** Nothing. This is Plan 00 for a reason — build it first.
**Unlocks:** Plans 01, 02, 06, 07, 09

---

## Problem Statement

Every agent in Antigravity currently outputs prose. The code-reviewer returns a markdown
narrative. The security-auditor returns paragraphs. The test-engineer returns bullet lists.
When /ship runs all three in parallel, the merge step must parse natural language to extract
verdicts, severities, and findings. This is fragile. A differently-worded response breaks
the merge logic silently — the orchestrator accepts malformed output and continues.

No file-based agentic system has solved this. The solution is typed contracts: every agent
declares an output schema, every output is validated against that schema before passing to
the next step, and invalid outputs trigger a retry with a corrective prompt.

---

## Architecture Overview

```
User invokes /ship
      |
      v
.claude/commands/ship.md reads .agent/schemas/review-output.schema.json
      |
      v
Spawns code-reviewer, security-auditor, test-engineer (parallel)
      |
      v
Each agent outputs JSON matching its schema
      |
      v
.agent/scripts/validate_output.py validates each output
      |
      v
If VALID: pass to merge step
If INVALID: retry with schema-correction prompt (max 2 retries)
      |
      v
Merge step assembles typed findings into GO/NO-GO decision
```

---

## Phase 1 — Create the Schema Directory

### Step 1.1 — Create .agent/schemas/

```bash
mkdir -p .agent/schemas
```

### Step 1.2 — Create the base schema for all agent outputs

Create `.agent/schemas/base-output.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "base-output",
  "type": "object",
  "required": ["agent_id", "timestamp", "confidence", "status"],
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "The agent that produced this output (e.g. code-reviewer)"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of when output was produced"
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Agent confidence in its output (0.0 to 1.0)"
    },
    "status": {
      "type": "string",
      "enum": ["complete", "partial", "failed"],
      "description": "Whether the agent completed its analysis"
    }
  }
}
```

### Step 1.3 — Create the code-reviewer output schema

Create `.agent/schemas/code-review.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "code-review",
  "allOf": [{ "$ref": "base-output.schema.json" }],
  "required": ["verdict", "findings", "axes_evaluated"],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": ["APPROVE", "REQUEST_CHANGES"],
      "description": "Final merge decision"
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["severity", "axis", "location", "description", "fix"],
        "properties": {
          "severity": {
            "type": "string",
            "enum": ["CRITICAL", "IMPORTANT", "SUGGESTION"]
          },
          "axis": {
            "type": "string",
            "enum": ["correctness", "readability", "architecture", "security", "performance"]
          },
          "location": {
            "type": "string",
            "description": "file:line or component name"
          },
          "description": {
            "type": "string",
            "minLength": 20,
            "description": "What the problem is — minimum 20 chars to prevent empty findings"
          },
          "fix": {
            "type": "string",
            "minLength": 20,
            "description": "Specific recommended fix — minimum 20 chars"
          }
        }
      }
    },
    "axes_evaluated": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["correctness", "readability", "architecture", "security", "performance"]
      },
      "minItems": 5,
      "description": "All five axes must be evaluated — none can be skipped"
    },
    "positive_observations": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "description": "At least one genuine positive finding required"
    }
  }
}
```

### Step 1.4 — Create the security-auditor output schema

Create `.agent/schemas/security-audit.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "security-audit",
  "allOf": [{ "$ref": "base-output.schema.json" }],
  "required": ["decision", "findings", "categories_checked", "threat_landscape"],
  "properties": {
    "decision": {
      "type": "string",
      "enum": ["BLOCK_MERGE", "APPROVE_WITH_MITIGATIONS", "SECURE"]
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["severity", "category", "location", "vulnerability", "attack_vector", "mitigation"],
        "properties": {
          "severity": {
            "type": "string",
            "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
          },
          "category": {
            "type": "string",
            "enum": ["input_handling", "auth_authorization", "data_protection", "infrastructure", "third_party"]
          },
          "location": { "type": "string" },
          "vulnerability": { "type": "string", "minLength": 20 },
          "attack_vector": { "type": "string", "minLength": 20 },
          "mitigation": { "type": "string", "minLength": 20 },
          "proof_of_concept": {
            "type": "string",
            "description": "Required for CRITICAL and HIGH findings"
          }
        }
      }
    },
    "categories_checked": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["input_handling", "auth_authorization", "data_protection", "infrastructure", "third_party"]
      },
      "minItems": 5,
      "description": "All five OWASP categories must be checked"
    },
    "threat_landscape": {
      "type": "string",
      "minLength": 50,
      "description": "1-2 paragraph summary of the attack surface"
    }
  }
}
```

### Step 1.5 — Create the test-engineer output schema

Create `.agent/schemas/test-analysis.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "test-analysis",
  "allOf": [{ "$ref": "base-output.schema.json" }],
  "required": ["coverage_verdict", "recommended_tests", "quality_assessment"],
  "properties": {
    "coverage_verdict": {
      "type": "string",
      "enum": ["INADEQUATE", "NEEDS_EDGE_CASES", "ROBUST"]
    },
    "recommended_tests": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["priority", "name", "what_it_verifies", "why_it_matters", "test_location", "sketch"],
        "properties": {
          "priority": {
            "type": "string",
            "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
          },
          "name": { "type": "string" },
          "what_it_verifies": { "type": "string", "minLength": 20 },
          "why_it_matters": { "type": "string", "minLength": 20 },
          "test_location": { "type": "string" },
          "sketch": { "type": "string", "description": "Code sketch of the test" }
        }
      }
    },
    "quality_assessment": {
      "type": "object",
      "required": ["test_independence", "mock_placement", "names_as_specs"],
      "properties": {
        "test_independence": { "type": "string", "enum": ["GOOD", "PROBLEM"] },
        "mock_placement": { "type": "string", "enum": ["GOOD", "PROBLEM"] },
        "names_as_specs": { "type": "string", "enum": ["GOOD", "IMPROVE"] }
      }
    }
  }
}
```

### Step 1.6 — Create the /ship merge schema

Create `.agent/schemas/ship-decision.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "ship-decision",
  "type": "object",
  "required": ["decision", "blockers", "recommended_fixes", "rollback_plan", "persona_summaries"],
  "properties": {
    "decision": {
      "type": "string",
      "enum": ["GO", "NO_GO"],
      "description": "Final ship decision"
    },
    "blockers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Findings that caused NO_GO — empty if GO"
    },
    "recommended_fixes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "rollback_plan": {
      "type": "string",
      "minLength": 30
    },
    "persona_summaries": {
      "type": "object",
      "required": ["code_reviewer", "security_auditor", "test_engineer"],
      "properties": {
        "code_reviewer": { "$ref": "code-review.schema.json" },
        "security_auditor": { "$ref": "security-audit.schema.json" },
        "test_engineer": { "$ref": "test-analysis.schema.json" }
      }
    }
  }
}
```

---

## Phase 2 — Build the Validation Engine

### Step 2.1 — Install the dependency

```bash
pip install jsonschema
```

Add `jsonschema` to a requirements.txt at repo root (create it if it doesn't exist):
```
jsonschema>=4.0.0
```

### Step 2.2 — Create .agent/scripts/validate_output.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Typed Output Validator
=============================================
Location: .agent/scripts/validate_output.py

Validates agent output JSON against the declared schema.
Used by /ship and any workflow that consumes agent outputs.

Usage:
  python .agent/scripts/validate_output.py --agent code-reviewer --input output.json
  python .agent/scripts/validate_output.py --agent security-auditor --input output.json
  python .agent/scripts/validate_output.py --agent test-engineer --input output.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_DIR = os.path.join(BASE, ".agent", "schemas")

AGENT_SCHEMA_MAP = {
    "code-reviewer":    "code-review.schema.json",
    "security-auditor": "security-audit.schema.json",
    "test-engineer":    "test-analysis.schema.json",
    "ship":             "ship-decision.schema.json",
}


def load_schema(schema_name: str) -> dict:
    schema_path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_output(agent_id: str, output_data: dict) -> tuple[bool, list[str]]:
    """
    Validate agent output against its schema.
    Returns (is_valid: bool, errors: list[str])
    """
    schema_name = AGENT_SCHEMA_MAP.get(agent_id)
    if not schema_name:
        return False, [f"No schema registered for agent: {agent_id}"]

    try:
        schema = load_schema(schema_name)
    except FileNotFoundError as e:
        return False, [str(e)]

    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(output_data):
        path = " -> ".join(str(p) for p in error.absolute_path) or "root"
        errors.append(f"[{path}] {error.message}")

    return len(errors) == 0, errors


def generate_correction_prompt(agent_id: str, errors: list[str], original_output: str) -> str:
    """
    Generate a targeted correction prompt when validation fails.
    This is injected back into the agent to fix its output.
    """
    schema_name = AGENT_SCHEMA_MAP.get(agent_id, "unknown")
    error_list = "\n".join(f"  - {e}" for e in errors)

    return f"""Your previous output failed schema validation for agent '{agent_id}'.
Schema: .agent/schemas/{schema_name}

Validation errors:
{error_list}

REQUIRED: Re-output your analysis as valid JSON matching the schema exactly.
Do not include markdown fences. Output only raw JSON.
Fix EVERY validation error listed above.
Original output for reference:
{original_output[:500]}...
"""


def main():
    parser = argparse.ArgumentParser(description="Validate agent output against schema")
    parser.add_argument("--agent", required=True, choices=list(AGENT_SCHEMA_MAP.keys()))
    parser.add_argument("--input", required=True, help="Path to JSON output file")
    parser.add_argument("--quiet", action="store_true", help="Only output VALID or INVALID")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"INVALID — Not valid JSON: {e}")
            sys.exit(1)

    is_valid, errors = validate_output(args.agent, output_data)

    if args.quiet:
        print("VALID" if is_valid else "INVALID")
        sys.exit(0 if is_valid else 1)

    if is_valid:
        print(f"VALID — {args.agent} output matches schema.")
        print(f"  Confidence: {output_data.get('confidence', 'N/A')}")
        print(f"  Status: {output_data.get('status', 'N/A')}")
        sys.exit(0)
    else:
        print(f"INVALID — {args.agent} output has {len(errors)} schema violation(s):")
        for err in errors:
            print(f"  ERROR: {err}")
        print()
        print("--- CORRECTION PROMPT ---")
        print(generate_correction_prompt(args.agent, errors, json.dumps(output_data)))
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Update Agent Persona Files

### Step 3.1 — Update .claude/agents/code-reviewer.md

At the END of the file, append this section:

```markdown
## Output Contract

You MUST output your findings as valid JSON matching `.agent/schemas/code-review.schema.json`.
Output ONLY raw JSON — no markdown fences, no prose before or after.

Before outputting, verify:
- [ ] `verdict` is "APPROVE" or "REQUEST_CHANGES"
- [ ] `findings` array has all required fields (severity, axis, location, description, fix)
- [ ] `axes_evaluated` lists all five axes
- [ ] `positive_observations` has at least one entry
- [ ] `confidence` is a decimal between 0.0 and 1.0
- [ ] `timestamp` is ISO 8601 format

Example minimal valid output:
{
  "agent_id": "code-reviewer",
  "timestamp": "2026-05-09T10:00:00Z",
  "confidence": 0.87,
  "status": "complete",
  "verdict": "REQUEST_CHANGES",
  "axes_evaluated": ["correctness", "readability", "architecture", "security", "performance"],
  "findings": [
    {
      "severity": "CRITICAL",
      "axis": "security",
      "location": "src/auth.ts:42",
      "description": "User input passed directly to SQL query without parameterization.",
      "fix": "Replace string concatenation with parameterized query: db.query('SELECT * FROM users WHERE id = ?', [userId])"
    }
  ],
  "positive_observations": ["Error handling is thorough across all async operations."]
}
```

Append the same output contract section to `security-auditor.md` and `test-engineer.md`,
referencing their respective schemas.

---

## Phase 4 — Update the /ship Command

### Step 4.1 — Update .claude/commands/ship.md

Replace the current merge step description with this validated merge protocol:

```markdown
## Validated Merge Protocol

PHASE A — Parallel fan-out (all three concurrently):
  1. code-reviewer: output JSON matching .agent/schemas/code-review.schema.json
  2. security-auditor: output JSON matching .agent/schemas/security-audit.schema.json
  3. test-engineer: output JSON matching .agent/schemas/test-analysis.schema.json

PHASE B — Validation:
  For each agent output, run:
    python .agent/scripts/validate_output.py --agent [agent-id] --input [output-file]
  
  If INVALID on first attempt:
    Inject the correction prompt (printed by validate_output.py) back to the agent.
    Re-run. Maximum 2 retries.
  
  If still INVALID after 2 retries:
    Report: "Agent [name] failed schema validation after 2 retries. /ship aborted."
    Do NOT proceed to merge with invalid data.

PHASE C — Typed merge:
  Extract from validated JSON:
  - All CRITICAL findings from code-reviewer.findings where severity == "CRITICAL"
  - All CRITICAL/HIGH findings from security-auditor.findings
  - All CRITICAL recommended_tests from test-engineer
  
  Blockers = union of all CRITICAL findings
  
  Decision rule:
    If len(blockers) > 0: decision = "NO_GO"
    If security-auditor.decision == "BLOCK_MERGE": decision = "NO_GO"
    Else: decision = "GO"

PHASE D — Output ship-decision.schema.json compliant result
```

---

## Phase 5 — Add Schema Registry to sync_registry.py

### Step 5.1 — Extend sync_registry.py

Add to the disk scan section:

```python
# Schema registry
disk_schemas = get_files(os.path.join(".agent", "schemas"))
state["installed_schemas"] = disk_schemas
state["component_counts"]["schemas"] = len(disk_schemas)
```

Add to AGENTS.md regeneration:
```python
schema_section = "\n## Schemas (Typed Contracts)\n\n"
for s in disk_schemas:
    schema_section += f"- `{s}`: output contract for {s.replace('.schema.json','')}\n"
```

---

## Phase 6 — Create the New Workflow

Create `.agent/workflows/25-typed-validation.md`:

```markdown
---
title: "TYPED VALIDATION"
description: "Validate agent output against JSON schema contracts."
order: 25
---

# Workflow: Typed Validation

**Objective:** Ensure agent outputs conform to their declared schemas before
being consumed by downstream steps.

## Trigger
- Called by /ship after each agent completes
- Called by any workflow that consumes structured agent output
- Manually: python .agent/scripts/validate_output.py --agent [name] --input [file]

## Steps
1. Run validate_output.py for each agent that ran
2. If VALID: proceed to merge step
3. If INVALID: inject correction prompt, retry (max 2 attempts)
4. If INVALID after retries: abort the parent workflow and report schema violation
5. Log validation result to .agent/data/telemetry.jsonl (when Plan 09 is implemented)

## Output
Validated JSON files for each agent, ready for typed merge.
```

---

## Verification

After completing all phases, verify:

```bash
# 1. Validate the schemas themselves are valid JSON
python -c "import json; [json.load(open(f'.agent/schemas/{s}')) for s in ['code-review.schema.json','security-audit.schema.json','test-analysis.schema.json']]"
echo "Schemas: VALID JSON"

# 2. Test the validator with a known-good input
echo '{"agent_id":"code-reviewer","timestamp":"2026-01-01T00:00:00Z","confidence":0.85,"status":"complete","verdict":"APPROVE","axes_evaluated":["correctness","readability","architecture","security","performance"],"findings":[],"positive_observations":["Clean code."]}' > /tmp/test_output.json
python .agent/scripts/validate_output.py --agent code-reviewer --input /tmp/test_output.json
# Expected: VALID

# 3. Test the validator with a known-bad input
echo '{"verdict":"APPROVE"}' > /tmp/bad_output.json
python .agent/scripts/validate_output.py --agent code-reviewer --input /tmp/bad_output.json
# Expected: INVALID with correction prompt

# 4. Run /sync-registry to register schemas in AGENTS.md
python .agent/scripts/sync_registry.py --no-bump
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/schemas/base-output.schema.json` | NEW |
| `.agent/schemas/code-review.schema.json` | NEW |
| `.agent/schemas/security-audit.schema.json` | NEW |
| `.agent/schemas/test-analysis.schema.json` | NEW |
| `.agent/schemas/ship-decision.schema.json` | NEW |
| `.agent/scripts/validate_output.py` | NEW |
| `.agent/workflows/25-typed-validation.md` | NEW |
| `.claude/agents/code-reviewer.md` | UPDATED (output contract appended) |
| `.claude/agents/security-auditor.md` | UPDATED (output contract appended) |
| `.claude/agents/test-engineer.md` | UPDATED (output contract appended) |
| `.claude/commands/ship.md` | UPDATED (validated merge protocol) |
| `.agent/scripts/sync_registry.py` | UPDATED (schema registry added) |
| `requirements.txt` | NEW or UPDATED |

---

## Learning Resources
- JSON Schema specification: https://json-schema.org/understanding-json-schema/
- Python jsonschema library: https://python-jsonschema.readthedocs.io/
- TypeChat (typed LLM outputs): https://github.com/microsoft/TypeChat
- instructor library: https://github.com/jxnl/instructor
