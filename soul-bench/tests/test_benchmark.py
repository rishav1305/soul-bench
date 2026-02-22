"""Tests for benchmark runner scoring and formatting logic."""
import json
import pytest
from pathlib import Path
import sys

# Add scripts to path so we can import benchmark
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import benchmark


class TestDetectModelFamily:
    def test_phi_model(self):
        assert benchmark.detect_model_family("Phi-3.5-mini-instruct-Q4_K_M.gguf") == "phi"

    def test_qwen_model(self):
        assert benchmark.detect_model_family("qwen2.5-3b-instruct-q4_k_m.gguf") == "qwen"

    def test_unknown_defaults_to_qwen(self):
        assert benchmark.detect_model_family("some-random-model.gguf") == "qwen"

    def test_case_insensitive(self):
        assert benchmark.detect_model_family("PHI-3.5-MINI.gguf") == "phi"
        assert benchmark.detect_model_family("QWEN2.5-3B.gguf") == "qwen"


class TestFormatPrompt:
    def test_phi_template(self):
        result = benchmark.format_prompt("Hello", "phi")
        assert result == "<|user|>\nHello<|end|>\n<|assistant|>\n"

    def test_qwen_template(self):
        result = benchmark.format_prompt("Hello", "qwen")
        assert result == "<|im_start|>user\nHello<|im_end|>\n<|im_start|>assistant\n"


class TestScoreResult:
    def test_exact_match_number_pass(self):
        prompt = {"expected_answer": "9", "scoring": "exact_match_number"}
        assert benchmark.score_result("The answer is 9.", prompt) == 1.0

    def test_exact_match_number_fail(self):
        prompt = {"expected_answer": "9", "scoring": "exact_match_number"}
        assert benchmark.score_result("The answer is 7.", prompt) == 0.0

    def test_contains_function_pass(self):
        prompt = {"expected_answer": "def is_palindrome", "scoring": "contains_function"}
        assert benchmark.score_result("def is_palindrome(s):\n    return s == s[::-1]", prompt) == 1.0

    def test_contains_function_fail(self):
        prompt = {"expected_answer": "def is_palindrome", "scoring": "contains_function"}
        assert benchmark.score_result("Here is a palindrome checker", prompt) == 0.0

    def test_exact_match_label_pass(self):
        prompt = {"expected_answer": "SPAM", "scoring": "exact_match_label"}
        assert benchmark.score_result("SPAM", prompt) == 1.0

    def test_exact_match_label_case_insensitive(self):
        prompt = {"expected_answer": "SPAM", "scoring": "exact_match_label"}
        assert benchmark.score_result("spam", prompt) == 1.0

    def test_exact_match_label_fail(self):
        prompt = {"expected_answer": "SPAM", "scoring": "exact_match_label"}
        assert benchmark.score_result("NOT_SPAM", prompt) == 0.0

    def test_unknown_scoring_returns_zero(self):
        prompt = {"expected_answer": "x", "scoring": "unknown_method"}
        assert benchmark.score_result("x", prompt) == 0.0


class TestSmokeTestPrompts:
    def test_prompts_file_valid_json(self):
        prompts_path = Path(__file__).parent.parent / "prompts" / "smoke-test.json"
        with open(prompts_path) as f:
            prompts = json.load(f)
        assert len(prompts) == 3

    def test_prompts_have_required_fields(self):
        prompts_path = Path(__file__).parent.parent / "prompts" / "smoke-test.json"
        with open(prompts_path) as f:
            prompts = json.load(f)
        for p in prompts:
            assert "id" in p
            assert "task" in p
            assert "prompt" in p
            assert "expected_answer" in p
            assert "scoring" in p

    def test_prompts_cover_three_tasks(self):
        prompts_path = Path(__file__).parent.parent / "prompts" / "smoke-test.json"
        with open(prompts_path) as f:
            prompts = json.load(f)
        tasks = {p["task"] for p in prompts}
        assert tasks == {"reasoning", "code", "classification"}
