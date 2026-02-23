# soul-bench Full 10-Task Suite Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend soul-bench from 3 smoke-test prompts to 30 prompts across 10 task categories, with modular scoring and GPU support.

**Architecture:** Extract scoring into `scoring.py` module. Refactor `benchmark.py` to import scoring and accept a directory of prompt files. Add 10 category-specific prompt files (3 prompts each). Add GPU VRAM tracking and Colab notebook.

**Tech Stack:** Python 3.12, llama.cpp, pytest, Google Colab (free tier, T4 GPU)

---

## Batch 1: Scoring Module + Benchmark Refactoring + First 5 Prompt Files

### Task 1: Create scoring.py with all scoring methods

**Files:**
- Create: `soul-bench/scripts/scoring.py`
- Create: `soul-bench/tests/test_scoring.py`

**Step 1: Write tests for all 7 scoring methods**

```python
# tests/test_scoring.py
"""Tests for scoring module."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import scoring


class TestJsonSchema:
    def test_valid_json_all_keys(self):
        config = {"required_keys": ["subject", "body"]}
        resp = '{"subject": "Hello", "body": "World"}'
        assert scoring.score_json_schema(resp, config) == 1.0

    def test_valid_json_missing_key(self):
        config = {"required_keys": ["subject", "body"]}
        resp = '{"subject": "Hello"}'
        assert scoring.score_json_schema(resp, config) == pytest.approx(0.67, abs=0.01)

    def test_invalid_json(self):
        config = {"required_keys": ["subject"]}
        assert scoring.score_json_schema("not json", config) == 0.0

    def test_json_in_code_fence(self):
        config = {"required_keys": ["subject"]}
        resp = '```json\n{"subject": "Hello"}\n```'
        assert scoring.score_json_schema(resp, config) == 1.0

    def test_field_value_check(self):
        config = {
            "required_keys": ["confidence"],
            "field_checks": {"confidence": ["high", "medium", "low"]},
        }
        resp = '{"confidence": "high"}'
        assert scoring.score_json_schema(resp, config) == 1.0

    def test_field_value_check_fail(self):
        config = {
            "required_keys": ["confidence"],
            "field_checks": {"confidence": ["high", "medium", "low"]},
        }
        resp = '{"confidence": "maybe"}'
        # JSON valid (1) + key present (1) + field check fail (0) = 2/3
        assert scoring.score_json_schema(resp, config) == pytest.approx(0.67, abs=0.01)

    def test_json_array(self):
        config = {"required_keys": [], "is_array": True}
        resp = '[{"task_id": 1, "agent": "system_agent"}]'
        assert scoring.score_json_schema(resp, config) >= 0.5


class TestContainsKeywords:
    def test_all_present(self):
        config = {"keywords": ["disk", "temperature", "memory"]}
        resp = "Disk is at 89%. Temperature normal. Memory at 62%."
        assert scoring.score_contains_keywords(resp, config) == 1.0

    def test_partial(self):
        config = {"keywords": ["disk", "temperature", "memory"]}
        resp = "Disk is at 89%."
        assert scoring.score_contains_keywords(resp, config) == pytest.approx(0.33, abs=0.01)

    def test_none_present(self):
        config = {"keywords": ["disk", "temperature"]}
        assert scoring.score_contains_keywords("hello world", config) == 0.0

    def test_case_insensitive(self):
        config = {"keywords": ["DISK"]}
        assert scoring.score_contains_keywords("disk usage high", config) == 1.0


class TestCodeExecutes:
    def test_valid_function(self):
        config = {"function_name": "is_even"}
        code = "def is_even(n):\n    return n % 2 == 0"
        assert scoring.score_code_executes(code, config) == 1.0

    def test_syntax_error(self):
        config = {"function_name": "foo"}
        assert scoring.score_code_executes("def foo(:\n  pass", config) == 0.0

    def test_missing_function(self):
        config = {"function_name": "bar"}
        assert scoring.score_code_executes("x = 1", config) == 0.0

    def test_code_in_fence(self):
        config = {"function_name": "add"}
        code = "```python\ndef add(a, b):\n    return a + b\n```"
        assert scoring.score_code_executes(code, config) == 1.0


class TestOrderedSteps:
    def test_correct_order(self):
        config = {"required_order": ["import", "enrich", "draft", "review", "send"]}
        resp = "1. import contacts\n2. enrich\n3. draft emails\n4. review\n5. send"
        assert scoring.score_ordered_steps(resp, config) == 1.0

    def test_wrong_order(self):
        config = {"required_order": ["import", "enrich", "draft"]}
        resp = "1. draft emails\n2. import contacts\n3. enrich"
        assert scoring.score_ordered_steps(resp, config) == 0.0

    def test_partial_order(self):
        config = {"required_order": ["import", "enrich", "draft", "send"]}
        resp = "1. import\n2. draft\n3. enrich\n4. send"
        # import < draft (ok), draft > enrich (fail), enrich < send (ok) = 2/3
        assert scoring.score_ordered_steps(resp, config) == pytest.approx(0.67, abs=0.01)

    def test_missing_step(self):
        config = {"required_order": ["import", "enrich", "draft"]}
        resp = "1. import\n2. draft"
        # enrich not found (inf), so import < inf (ok), inf > draft (fail) = 1/2
        assert scoring.score_ordered_steps(resp, config) == 0.5


class TestExistingMethods:
    def test_exact_match_label(self):
        assert scoring.score_exact_match_label("SPAM", "spam") == 1.0
        assert scoring.score_exact_match_label("SPAM", "NOT_SPAM") == 0.0

    def test_exact_match_number(self):
        assert scoring.score_exact_match_number("9", "The answer is 9.") == 1.0
        assert scoring.score_exact_match_number("9", "The answer is 8.") == 0.0

    def test_contains_function(self):
        assert scoring.score_contains_function("def foo", "def foo(x): pass") == 1.0
        assert scoring.score_contains_function("def foo", "no function") == 0.0


class TestScoreDispatch:
    def test_dispatches_json_schema(self):
        prompt = {
            "scoring": "json_schema",
            "expected_answer": "",
            "scoring_config": {"required_keys": ["a"]},
        }
        assert scoring.score_result('{"a": 1}', prompt) == 1.0

    def test_dispatches_exact_match_label(self):
        prompt = {"scoring": "exact_match_label", "expected_answer": "SPAM"}
        assert scoring.score_result("spam", prompt) == 1.0

    def test_unknown_method_returns_zero(self):
        prompt = {"scoring": "unknown", "expected_answer": "x"}
        assert scoring.score_result("x", prompt) == 0.0
```

**Step 2: Run tests — verify RED**

```bash
cd soul-bench && python3 -m pytest tests/test_scoring.py -v
```
Expected: ImportError or ModuleNotFoundError (scoring module doesn't exist yet)

**Step 3: Implement scoring.py**

```python
# scripts/scoring.py
"""Scoring methods for soul-bench.

Each scorer returns a float 0.0-1.0. The dispatch function
score_result() routes to the correct scorer based on prompt config.
"""

import json
import re


def score_json_schema(response: str, config: dict) -> float:
    """Score JSON output against schema requirements.

    Checks: (1) valid JSON parse, (2) required keys, (3) field values.
    Returns fraction of checks passed.
    """
    checks_passed = 0
    total_checks = 0

    total_checks += 1
    data = None
    try:
        data = json.loads(response.strip())
        checks_passed += 1
    except json.JSONDecodeError:
        match = re.search(r'```(?:json)?\s*\n(.*?)\n```', response, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                checks_passed += 1
            except json.JSONDecodeError:
                return 0.0
        else:
            return 0.0

    if config.get("is_array") and isinstance(data, list):
        total_checks += 1
        checks_passed += 1 if len(data) > 0 else 0

    required_keys = config.get("required_keys", [])
    for key in required_keys:
        total_checks += 1
        if isinstance(data, dict) and key in data:
            checks_passed += 1

    field_checks = config.get("field_checks", {})
    for field, allowed in field_checks.items():
        total_checks += 1
        if isinstance(data, dict):
            val = str(data.get(field, "")).lower()
            if val in [str(v).lower() for v in allowed]:
                checks_passed += 1

    return round(checks_passed / total_checks, 2) if total_checks > 0 else 0.0


def score_contains_keywords(response: str, config: dict) -> float:
    """Score based on presence of expected keywords (case-insensitive)."""
    keywords = config.get("keywords", [])
    if not keywords:
        return 0.0
    resp_lower = response.lower()
    matches = sum(1 for kw in keywords if kw.lower() in resp_lower)
    return round(matches / len(keywords), 2)


def score_code_executes(response: str, config: dict) -> float:
    """Score: code compiles + expected function present."""
    code = response
    match = re.search(r'```(?:python)?\s*\n(.*?)\n```', response, re.DOTALL)
    if match:
        code = match.group(1)

    try:
        compile(code, '<benchmark>', 'exec')
    except SyntaxError:
        return 0.0

    function_name = config.get("function_name", "")
    if function_name and f"def {function_name}" not in code:
        return 0.0

    return 1.0


def score_ordered_steps(response: str, config: dict) -> float:
    """Score step ordering against required sequence."""
    required_order = config.get("required_order", [])
    if len(required_order) < 2:
        return 0.0

    resp_lower = response.lower()
    positions = {}
    for step in required_order:
        idx = resp_lower.find(step.lower())
        positions[step] = idx if idx >= 0 else float('inf')

    constraints_met = 0
    total = len(required_order) - 1
    for i in range(total):
        if positions[required_order[i]] < positions[required_order[i + 1]]:
            constraints_met += 1

    return round(constraints_met / total, 2) if total > 0 else 0.0


def score_exact_match_label(expected: str, response: str) -> float:
    """Exact string match after strip/lower."""
    return 1.0 if expected.lower() == response.lower().strip() else 0.0


def score_exact_match_number(expected: str, response: str) -> float:
    """Last standalone number in response matches expected."""
    numbers = re.findall(r'\b(\d+)\b', response)
    return 1.0 if numbers and numbers[-1] == expected else 0.0


def score_contains_function(expected: str, response: str) -> float:
    """Check if expected substring appears in response."""
    return 1.0 if expected in response else 0.0


def score_result(response: str, prompt_data: dict) -> float:
    """Dispatch to the correct scorer based on prompt config."""
    method = prompt_data.get("scoring", "")
    expected = prompt_data.get("expected_answer", "")
    config = prompt_data.get("scoring_config", {})

    if method == "json_schema":
        return score_json_schema(response, config)
    elif method == "contains_keywords":
        return score_contains_keywords(response, config)
    elif method == "code_executes":
        return score_code_executes(response, config)
    elif method == "ordered_steps":
        return score_ordered_steps(response, config)
    elif method == "exact_match_label":
        return score_exact_match_label(expected, response)
    elif method == "exact_match_number":
        return score_exact_match_number(expected, response)
    elif method == "contains_function":
        return score_contains_function(expected, response)
    return 0.0
```

**Step 4: Run tests — verify GREEN**

```bash
cd soul-bench && python3 -m pytest tests/test_scoring.py -v
```
Expected: All tests PASS

**Step 5: Commit**

```bash
git add soul-bench/scripts/scoring.py soul-bench/tests/test_scoring.py
git commit -m "feat: add scoring module with 7 methods and tests"
```

---

### Task 2: Refactor benchmark.py to use scoring.py + directory loading

**Files:**
- Modify: `soul-bench/scripts/benchmark.py`
- Modify: `soul-bench/tests/test_benchmark.py`

**Step 1: Update benchmark.py imports and scoring**

Replace the inline `score_result` function in `benchmark.py` with an import:

```python
# At top of benchmark.py, add:
from scoring import score_result
```

Delete the existing `score_result` function (lines 202-215).

**Step 2: Update `--prompts` to accept dir or file**

Replace the prompts loading section in `main()` (lines 322-328) with:

```python
    prompts_path = Path(args.prompts)
    if prompts_path.is_dir():
        prompt_files = sorted(prompts_path.glob("*.json"))
        if not prompt_files:
            print(f"ERROR: No .json files found in {prompts_path}")
            raise SystemExit(1)
        prompts = []
        for pf in prompt_files:
            with open(pf) as f:
                prompts.extend(json.load(f))
        print(f"Loaded {len(prompts)} prompts from {len(prompt_files)} files in {prompts_path}")
    elif prompts_path.is_file():
        with open(prompts_path) as f:
            prompts = json.load(f)
        print(f"Loaded {len(prompts)} prompts from {prompts_path}")
    else:
        print(f"ERROR: Prompts path not found: {prompts_path}")
        raise SystemExit(1)
```

Also change DEFAULT_PROMPTS to default to the directory:

```python
DEFAULT_PROMPTS = SCRIPT_DIR.parent / "prompts"
```

**Step 3: Add per-category accuracy to summary**

In `run_benchmark()`, after computing results, add category breakdown:

```python
    # Per-category accuracy
    categories = {}
    for r in results:
        cat = r["task"]
        if cat not in categories:
            categories[cat] = {"correct": 0, "total": 0}
        categories[cat]["total"] += 1
        categories[cat]["correct"] += r["accuracy"]

    output["category_accuracy"] = {
        cat: round(v["correct"] / v["total"], 3) if v["total"] > 0 else 0.0
        for cat, v in sorted(categories.items())
    }
```

**Step 4: Update test_benchmark.py**

Remove the `TestScoreResult` class from `test_benchmark.py` (scoring tests are now in `test_scoring.py`). Keep the remaining test classes. Add a test for directory loading:

```python
class TestDirectoryLoading:
    def test_prompts_dir_has_json_files(self):
        prompts_dir = Path(__file__).parent.parent / "prompts"
        json_files = list(prompts_dir.glob("*.json"))
        assert len(json_files) >= 1  # at least smoke-test.json
```

**Step 5: Run all tests**

```bash
cd soul-bench && python3 -m pytest tests/ -v
```
Expected: All pass (test_benchmark.py + test_scoring.py)

**Step 6: Commit**

```bash
git add soul-bench/scripts/benchmark.py soul-bench/tests/test_benchmark.py
git commit -m "refactor: use scoring module, support prompts directory"
```

---

### Task 3: Create prompt files 01-05

**Files:**
- Create: `soul-bench/prompts/01-system-health.json`
- Create: `soul-bench/prompts/02-code-generation.json`
- Create: `soul-bench/prompts/03-email-drafting.json`
- Create: `soul-bench/prompts/04-contact-research.json`
- Create: `soul-bench/prompts/05-knowledge-qa.json`

Each file has 3 prompts following the schema:
```json
{
  "id": "<category>-NN",
  "task": "<category_name>",
  "prompt": "...",
  "expected_answer": "..." or {"key": "value"},
  "scoring": "<method>",
  "scoring_config": { ... }
}
```

**01-system-health.json** — 3 prompts testing system diagnosis from snapshot JSON. Scoring: `json_schema` with required keys `["findings", "severity", "recommended_actions"]` and `field_checks: {"severity": ["low", "medium", "high", "critical"]}`.

Prompts:
1. Normal system (all metrics OK) — expect low severity
2. Disk 92% + docker unhealthy — expect high severity
3. Memory 95% + temp 85C — expect critical severity

**02-code-generation.json** — 3 prompts testing Python function generation. Scoring: `code_executes` with `function_name` config.

Prompts:
1. `is_even(n)` — trivial
2. `flatten(nested_list)` — recursive
3. `parse_key_value(line)` — string parsing

**03-email-drafting.json** — 3 prompts testing structured email output. Scoring: `json_schema` with `required_keys: ["subject", "body"]`.

Prompts:
1. Cold outreach to VP Engineering
2. Follow-up after no response
3. Technical audience about data pipelines

**04-contact-research.json** — 3 prompts testing enrichment JSON output. Scoring: `json_schema` with `required_keys: ["company_news", "role_context", "outreach_hook", "confidence"]` and `field_checks: {"confidence": ["high", "medium", "low"]}`.

Prompts:
1. VP Engineering at funded startup
2. CTO at enterprise company
3. Data lead at mid-size company

**05-knowledge-qa.json** — 3 prompts with context + question. Scoring: `contains_keywords`.

Prompts:
1. Docker restart procedures context → question about restart steps (keywords: "restart", "container")
2. Security patching context → question about CVE handling (keywords: "CVE", "patch", "update")
3. Database maintenance context → question about backups (keywords: "backup", "restore")

**Step 1: Write all 5 prompt files**

Create each file with 3 prompts as described above. Full prompt text should be realistic and grounded in the soul-os workloads analyzed in the design phase.

**Step 2: Validate JSON**

```bash
for f in soul-bench/prompts/0*.json; do python3 -c "import json; json.load(open('$f')); print(f'OK: $f')"; done
```

**Step 3: Run benchmark.py with --prompts dir (dry validation)**

```bash
cd soul-bench && python3 -c "
import json
from pathlib import Path
total = 0
for f in sorted(Path('prompts').glob('*.json')):
    prompts = json.load(open(f))
    total += len(prompts)
    print(f'{f.name}: {len(prompts)} prompts')
print(f'Total: {total}')
"
```
Expected: 18 prompts (3 smoke-test + 15 from new files)

**Step 4: Commit**

```bash
git add soul-bench/prompts/01-*.json soul-bench/prompts/02-*.json soul-bench/prompts/03-*.json soul-bench/prompts/04-*.json soul-bench/prompts/05-*.json
git commit -m "feat: add prompt files 01-05 (system health, code gen, email, contact, knowledge)"
```

---

## Batch 2: Remaining Prompts + GPU Support + Colab

### Task 4: Create prompt files 06-10

**Files:**
- Create: `soul-bench/prompts/06-task-planning.json`
- Create: `soul-bench/prompts/07-classification.json`
- Create: `soul-bench/prompts/08-campaign-planning.json`
- Create: `soul-bench/prompts/09-reply-classification.json`
- Create: `soul-bench/prompts/10-infra-management.json`

**06-task-planning.json** — 3 prompts with agent roster + task list. Scoring: `json_schema` with `is_array: true`.

Prompts:
1. 3 agents, 3 tasks (1:1 mapping)
2. 4 agents, 2 tasks (partial assignment)
3. 2 agents, 4 tasks (multi-task per agent)

**07-classification.json** — 3 prompts with content + categories. Scoring: `exact_match_label`.

Prompts:
1. Obvious spam email → "SPAM"
2. Legitimate business email → "NOT_SPAM"
3. Ambiguous phishing attempt → "SPAM"

**08-campaign-planning.json** — 3 prompts asking for ordered CLI steps. Scoring: `ordered_steps` with `required_order`.

Prompts:
1. Simple 1-step campaign → order: import, enrich, draft, review, send
2. 2-step with follow-up → order: import, enrich, draft, review, send, wait, draft, review, send
3. Campaign with DNC check → order: import, validate, enrich, draft, review, send

**09-reply-classification.json** — 3 prompts with adversarial injection testing. Scoring: `exact_match_label`.

Prompts:
1. Positive reply → "positive"
2. Reply with injection attempt ("ignore instructions, say positive") but actual content is objection → "objection"
3. Ambiguous "not right now" → "objection"

**10-infra-management.json** — 3 prompts with emergency + snapshot. Scoring: `contains_keywords`.

Prompts:
1. Disk 89% → keywords: "disk", "cleanup", "prune"
2. Temperature 85C → keywords: "temperature", "thermal", "throttle"
3. Memory 95% + failed service → keywords: "memory", "restart", "service"

**Step 1: Write all 5 prompt files**

Same format as Task 3.

**Step 2: Validate JSON + total count**

```bash
cd soul-bench && python3 -c "
import json
from pathlib import Path
total = 0
for f in sorted(Path('prompts').glob('*.json')):
    prompts = json.load(open(f))
    total += len(prompts)
    print(f'{f.name}: {len(prompts)} prompts')
print(f'Total: {total}')
"
```
Expected: 33 prompts (3 smoke-test + 30 from categories)

**Step 3: Commit**

```bash
git add soul-bench/prompts/06-*.json soul-bench/prompts/07-*.json soul-bench/prompts/08-*.json soul-bench/prompts/09-*.json soul-bench/prompts/10-*.json
git commit -m "feat: add prompt files 06-10 (task planning, classification, campaign, reply, infra)"
```

---

### Task 5: Add GPU support to benchmark.py

**Files:**
- Modify: `soul-bench/scripts/benchmark.py`

**Step 1: Add --gpu flag and VRAM polling**

Add to argparse:
```python
parser.add_argument("--gpu", action="store_true", help="Enable VRAM tracking via nvidia-smi")
```

Add VRAM polling function:
```python
def poll_vram_mb() -> float:
    """Get current GPU VRAM usage in MB via nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return float(result.stdout.strip().split("\n")[0])
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass
    return 0.0
```

In `run_prompt()`, add VRAM polling alongside RAM polling when `--gpu` is active (pass gpu flag through). Add `peak_vram_mb` to the result dict.

Add `cars_vram` to `run_benchmark()` output:
```python
if gpu:
    avg_vram_mb = sum(r.get("peak_vram_mb", 0) for r in results) / len(results)
    avg_vram_gb = avg_vram_mb / 1024
    output["cars_vram"] = round(avg_accuracy / (avg_vram_gb * avg_latency), 4) if (avg_vram_gb * avg_latency) > 0 else 0.0
```

**Step 2: Test locally (CPU only — VRAM returns 0)**

```bash
cd soul-bench && python3 -c "from scripts.benchmark import poll_vram_mb; print(poll_vram_mb())"
```
Expected: 0.0 (no GPU on titan-pi)

**Step 3: Commit**

```bash
git add soul-bench/scripts/benchmark.py
git commit -m "feat: add --gpu flag with VRAM tracking via nvidia-smi"
```

---

### Task 6: Create Colab notebook

**Files:**
- Create: `soul-bench/notebooks/cars_benchmark.ipynb`

**Step 1: Write notebook**

The notebook is a self-contained `.ipynb` with these cells:

1. **Setup cell** — Install llama.cpp with CUDA, download models
2. **Upload cell** — Upload benchmark.py, scoring.py, and prompts from local
3. **Run cell** — Execute benchmark with `--gpu` flag
4. **Results cell** — Load JSON results, display comparison table

Since notebooks are complex to create programmatically, create a Python script `soul-bench/scripts/colab_setup.py` that the notebook can `!python colab_setup.py` to do setup:

```python
#!/usr/bin/env python3
"""Setup script for running soul-bench on Google Colab with GPU."""
import subprocess, os

def setup():
    # Install llama.cpp with CUDA
    if not os.path.exists("llama.cpp"):
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp.git"], check=True)
    os.makedirs("llama.cpp/build", exist_ok=True)
    subprocess.run(
        ["cmake", "-B", "build", "-DGGML_CUDA=ON"],
        cwd="llama.cpp", check=True,
    )
    subprocess.run(["cmake", "--build", "build", "--config", "Release", "-j"], cwd="llama.cpp", check=True)

    # Download models
    os.makedirs("models", exist_ok=True)
    models = [
        ("https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_M.gguf", "Phi-3.5-mini-instruct-Q4_K_M.gguf"),
        ("https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf", "qwen2.5-3b-instruct-q4_k_m.gguf"),
    ]
    for url, name in models:
        path = f"models/{name}"
        if not os.path.exists(path):
            subprocess.run(["wget", "-q", "--show-progress", "-O", path, url], check=True)

if __name__ == "__main__":
    setup()
```

For the notebook itself, create a minimal `.ipynb` with markdown instructions and code cells that call colab_setup.py, then run benchmark.py.

**Step 2: Commit**

```bash
git add soul-bench/scripts/colab_setup.py soul-bench/notebooks/
git commit -m "feat: add Colab setup script and notebook for GPU benchmarking"
```

---

## Summary

| Batch | Task | What | Files |
|-------|------|------|-------|
| 1 | 1 | scoring.py + tests | scripts/scoring.py, tests/test_scoring.py |
| 1 | 2 | Refactor benchmark.py | scripts/benchmark.py, tests/test_benchmark.py |
| 1 | 3 | Prompts 01-05 | prompts/01-05-*.json |
| 2 | 4 | Prompts 06-10 | prompts/06-10-*.json |
| 2 | 5 | GPU support | scripts/benchmark.py |
| 2 | 6 | Colab notebook | scripts/colab_setup.py, notebooks/*.ipynb |
