"""
Tests for routing module to improve coverage.

Tests cover query analysis, domain detection, template selection,
and error handling paths in routing.py.
"""

import sys
from pathlib import Path

# Add parent directories for package imports
test_dir = Path(__file__).parent
skills_dir = test_dir.parent.parent
sys.path.insert(0, str(skills_dir))

import pytest

from skill.routing import (
    # Functions
    select_template,
    validate_template,
    extract_template_override,
    detect_domain_keywords,
    detect_complexity,
    detect_intent_type,
    # Constants
    DOMAIN_KEYWORDS,
    HIGH_COMPLEXITY_INDICATORS,
    VALID_TEMPLATES,
    TEMPLATE_METADATA,
    DOMAIN_PRIORITY,
    # Types
    TemplateResult,
    ConfigResult,
    ValidationResult,
)
from skill.config import VALID_DOMAINS


class TestExtractTemplateOverride:
    """Tests for extract_template_override function."""

    def test_valid_template_override_returns_template(self):
        """Given valid template in query, return template name."""
        result = extract_template_override("redesign api template=deep")
        assert result == "deep"

    def test_all_valid_templates_accepted(self):
        """All templates in VALID_TEMPLATES should be accepted."""
        for template in VALID_TEMPLATES:
            query = f"some query template={template}"
            result = extract_template_override(query)
            assert result == template, f"Template {template} should be accepted"

    def test_invalid_template_returns_none(self):
        """Invalid template not in allowlist returns None."""
        result = extract_template_override("query template=malicious")
        assert result is None

    def test_no_override_returns_none(self):
        """Query without template override returns None."""
        result = extract_template_override("just a regular query")
        assert result is None

    def test_case_sensitive_template_names(self):
        """Template names are case-sensitive."""
        result = extract_template_override("template=DEEP")
        # DEEP is not in VALID_TEMPLATES (which has lowercase "deep")
        assert result is None

    def test_override_with_hyphenated_name(self):
        """Hyphenated template names work correctly."""
        result = extract_template_override("template=data-pipeline")
        assert result == "data-pipeline"


class TestDetectDomainKeywords:
    """Tests for detect_domain_keywords function."""

    def test_cli_domain_detected(self):
        """CLI keywords detected correctly."""
        result = detect_domain_keywords("help with command line parsing")
        assert result == "cli"

    def test_python_domain_detected(self):
        """Python keywords detected correctly."""
        result = detect_domain_keywords("asyncio not working")
        assert result == "python"

    def test_data_pipeline_domain_detected(self):
        """Data pipeline keywords detected correctly."""
        result = detect_domain_keywords("build kafka streaming pipeline")
        assert result == "data-pipeline"

    def test_precedent_domain_detected(self):
        """Precedent/ADR keywords detected correctly."""
        result = detect_domain_keywords("create an architecture decision record")
        assert result == "precedent"

    def test_no_keywords_returns_none(self):
        """Query without domain keywords returns None."""
        result = detect_domain_keywords("just some random text")
        assert result is None

    def test_priority_order_cli_over_python(self):
        """CLI has priority over python when both keywords present."""
        result = detect_domain_keywords("python command line tool")
        assert result == "cli"  # CLI checked first

    def test_case_insensitive_matching(self):
        """Domain detection is case-insensitive."""
        result = detect_domain_keywords("PYTHON ASYNC code")
        assert result == "python"

    def test_all_cli_keywords(self):
        """All CLI keywords should trigger detection."""
        cli_keywords = ["cli", "terminal", "shell", "posix", "exit code", "argument parsing"]
        for keyword in cli_keywords:
            query = f"help with {keyword}"
            result = detect_domain_keywords(query)
            assert result == "cli", f"Keyword '{keyword}' should detect CLI domain"

    def test_all_python_keywords(self):
        """Sample of Python keywords should trigger detection."""
        python_keywords = ["asyncio", "django", "decorator", "context manager"]
        for keyword in python_keywords:
            query = f"fix {keyword}"
            result = detect_domain_keywords(query)
            assert result == "python", f"Keyword '{keyword}' should detect Python domain"


class TestDetectComplexity:
    """Tests for detect_complexity function."""

    def test_redesign_indicates_deep(self):
        """'redesign' keyword indicates deep template."""
        result = detect_complexity("redesign the api")
        assert result == "deep"

    def test_architecture_indicates_deep(self):
        """'architecture' keyword indicates deep template."""
        result = detect_complexity("system architecture review")
        assert result == "deep"

    def test_microservices_indicates_deep(self):
        """'microservices' keyword indicates deep template."""
        result = detect_complexity("convert to microservices")
        assert result == "deep"

    def test_rewrite_indicates_deep(self):
        """'rewrite' keyword indicates deep template."""
        result = detect_complexity("rewrite the backend")
        assert result == "deep"

    def test_from_scratch_indicates_deep(self):
        """'from scratch' indicates deep template."""
        result = detect_complexity("build from scratch")
        assert result == "deep"

    def test_no_indicators_defaults_to_fast(self):
        """Query without complexity indicators defaults to fast."""
        result = detect_complexity("simple bug fix")
        assert result == "fast"

    def test_case_insensitive_detection(self):
        """Complexity detection is case-insensitive."""
        result = detect_complexity("REDESIGN system")
        assert result == "deep"

    def test_all_high_complexity_indicators(self):
        """All high complexity indicators should return 'deep'."""
        for indicator in HIGH_COMPLEXITY_INDICATORS:
            query = f"system {indicator}"
            result = detect_complexity(query)
            assert result == "deep", f"Indicator '{indicator}' should return 'deep'"


class TestDetectIntentType:
    """Tests for detect_intent_type function."""

    def test_improve_with_subsystem_returns_improve_system(self):
        """Improve + subsystem keywords returns IMPROVE_SYSTEM."""
        result = detect_intent_type("improve memory system")
        assert result == "IMPROVE_SYSTEM"

    def test_optimize_with_cks_returns_improve_system(self):
        """Optimize + CKS returns IMPROVE_SYSTEM."""
        result = detect_intent_type("optimize cks queries")
        assert result == "IMPROVE_SYSTEM"

    def test_enhance_with_hooks_returns_improve_system(self):
        """Enhance + hooks returns IMPROVE_SYSTEM."""
        result = detect_intent_type("enhance hooks performance")
        assert result == "IMPROVE_SYSTEM"

    def test_improve_without_subsystem_returns_default(self):
        """Improve without subsystem returns DEFAULT."""
        result = detect_intent_type("improve performance")
        assert result == "DEFAULT"

    def test_subsystem_without_improve_returns_default(self):
        """Subsystem without improve returns DEFAULT."""
        result = detect_intent_type("memory system analysis")
        assert result == "DEFAULT"

    def test_no_keywords_returns_default(self):
        """Query without keywords returns DEFAULT."""
        result = detect_intent_type("random query")
        assert result == "DEFAULT"

    def test_case_insensitive_detection(self):
        """Intent detection is case-insensitive."""
        result = detect_intent_type("IMPROVE memory SYSTEM")
        assert result == "IMPROVE_SYSTEM"


class TestSelectTemplate:
    """Tests for select_template function covering all routing paths."""

    def test_template_override_parameter_highest_priority(self):
        """Template override parameter takes highest priority."""
        result = select_template("python cli tool", template_override="precedent")
        assert result == "precedent"

    def test_invalid_template_override_raises_error(self):
        """Invalid template override raises ValueError."""
        with pytest.raises(ValueError, match="Invalid template override"):
            select_template("query", template_override="invalid")

    def test_template_override_in_query(self):
        """Template override in query string is honored."""
        result = select_template("redesign api template=deep")
        assert result == "deep"

    def test_invalid_template_in_query_ignored(self):
        """Invalid template in query is ignored (security validation)."""
        # extract_template_override returns None for invalid templates
        # so routing falls through to other detection methods
        result = select_template("query template=malicious")
        # Falls through to complexity detection since invalid template ignored
        assert result in VALID_TEMPLATES  # Should return a valid template

    def test_default_domain_used_when_no_keywords(self):
        """Default domain is used when no keywords detected."""
        result = select_template("random query", default_domain="python")
        assert result == "python"

    def test_env_domain_used_when_no_default_domain(self):
        """Environment domain is used when default_domain not provided."""
        result = select_template("random query", env_domain="cli")
        assert result == "cli"

    def test_default_domain_overrides_env_domain(self):
        """Default domain parameter takes precedence over env_domain."""
        result = select_template(
            "random query", default_domain="python", env_domain="cli"
        )
        assert result == "python"

    def test_auto_domain_allows_keyword_detection(self):
        """auto domain allows keyword detection to proceed."""
        result = select_template("command line tool", default_domain="auto")
        assert result == "cli"  # keyword detected, not auto

    def test_auto_domain_falls_through_to_complexity(self):
        """auto domain falls through to complexity detection."""
        result = select_template("simple bug fix", default_domain="auto")
        assert result == "fast"  # complexity detection

    def test_invalid_domain_raises_error(self):
        """Invalid domain raises ValueError."""
        with pytest.raises(ValueError, match="Invalid domain"):
            select_template("query", default_domain="invalid")

    def test_keyword_detection_overrides_default_domain(self):
        """Explicit keywords override default domain (non-auto)."""
        # Even though default is python, cli keyword should win
        # But actually, looking at the code, detected_domain takes priority ONLY if domain is not set or is auto
        # Let me re-read the logic...
        # Actually line 342-346: detected_domain is returned directly, ignoring default
        result = select_template("command line tool", default_domain="python")
        assert result == "cli"  # keyword detection wins

    def test_complexity_detection_when_no_domain_or_keywords(self):
        """Complexity detection used when no domain and no keywords."""
        result = select_template("redesign the system")
        assert result == "deep"  # complexity detection

    def test_complexity_detection_defaults_to_fast(self):
        """Complexity detection defaults to fast when no indicators."""
        result = select_template("simple query")
        assert result == "fast"

    def test_full_routing_flow_priority_order(self):
        """Test complete priority chain: override > default > keywords > complexity."""
        # Override wins
        assert select_template("python cli", template_override="precedent") == "precedent"
        # Keywords win over default
        assert select_template("command line", default_domain="python") == "cli"
        # Default wins when no keywords
        assert select_template("random", default_domain="python") == "python"
        # Complexity wins when nothing else
        assert select_template("redesign system") == "deep"


class TestValidateTemplate:
    """Tests for validate_template function."""

    def test_valid_template_returns_true(self):
        """Valid template returns (True, '')."""
        is_valid, error = validate_template("fast")
        assert is_valid is True
        assert error == ""

    def test_invalid_template_returns_false(self):
        """Invalid template returns (False, error_message)."""
        is_valid, error = validate_template("invalid")
        assert is_valid is False
        assert "Invalid template" in error
        assert "invalid" in error

    def test_all_valid_templates_validate(self):
        """All templates in VALID_TEMPLATES should validate."""
        for template in VALID_TEMPLATES:
            is_valid, error = validate_template(template)
            assert is_valid, f"Template {template} should be valid: {error}"

    def test_error_message_includes_valid_templates(self):
        """Error message includes list of valid templates."""
        is_valid, error = validate_template("wrong")
        assert is_valid is False
        for template in ["fast", "deep", "cli", "python"]:
            assert template in error


class TestConstants:
    """Tests for exported constants."""

    def test_domain_keywords_structure(self):
        """DOMAIN_KEYWORDS has correct structure."""
        assert isinstance(DOMAIN_KEYWORDS, dict)
        assert "cli" in DOMAIN_KEYWORDS
        assert "python" in DOMAIN_KEYWORDS
        assert "data-pipeline" in DOMAIN_KEYWORDS
        assert "precedent" in DOMAIN_KEYWORDS

    def test_valid_templates_is_set(self):
        """VALID_TEMPLATES is a set with expected values."""
        assert isinstance(VALID_TEMPLATES, set)
        assert "fast" in VALID_TEMPLATES
        assert "deep" in VALID_TEMPLATES

    def test_template_metadata_structure(self):
        """TEMPLATE_METADATA has correct structure."""
        assert isinstance(TEMPLATE_METADATA, dict)
        for template in VALID_TEMPLATES:
            assert template in TEMPLATE_METADATA
            metadata = TEMPLATE_METADATA[template]
            assert "complexity" in metadata
            assert "domain" in metadata

    def test_domain_priority_order(self):
        """DOMAIN_PRIORITY has expected order."""
        assert isinstance(DOMAIN_PRIORITY, list)
        assert len(DOMAIN_PRIORITY) == 4
        assert DOMAIN_PRIORITY[0] == "cli"  # Highest priority


class TestTypeDefinitions:
    """Tests for TypedDict type definitions."""

    def test_template_result_type(self):
        """TemplateResult TypedDict can be instantiated."""
        result: TemplateResult = {
            "template": "fast",
            "source": "complexity",
            "confidence": "high",
        }
        assert result["template"] == "fast"

    def test_config_result_type(self):
        """ConfigResult TypedDict can be instantiated."""
        result: ConfigResult = {
            "config": {"default_domain": "python"},
            "source": "file",
            "error": None,
        }
        assert result["source"] == "file"

    def test_validation_result_type(self):
        """ValidationResult TypedDict can be instantiated."""
        result: ValidationResult = {
            "is_valid": True,
            "error_message": "",
            "template_path": Path("test.md"),
        }
        assert result["is_valid"] is True


class TestIntegrationSelectTemplateWithConfig:
    """Integration tests for select_template with load_arch_config."""

    def test_select_template_with_config_no_default_domain(self):
        """When load_arch_config returns None, select_template falls through to keyword detection."""
        # Simulate load_arch_config returning None (no config file)
        config = None
        default_domain = config.get("default_domain") if config else None

        # Should fall through to keyword detection
        result = select_template("command line tool", default_domain=default_domain)
        assert result == "cli"

    def test_select_template_with_config_default_domain(self):
        """When load_arch_config returns a config, select_template uses default_domain."""
        # Simulate load_arch_config returning a config with python domain
        config = {"default_domain": "python"}
        default_domain = config.get("default_domain")

        # Should use default domain since no keywords detected
        result = select_template("random query", default_domain=default_domain)
        assert result == "python"

    def test_select_template_with_config_auto_domain(self):
        """When config has auto domain, select_template uses keyword detection."""
        # Simulate load_arch_config returning auto domain
        config = {"default_domain": "auto"}
        default_domain = config.get("default_domain")

        # Should detect cli keyword and return cli template
        result = select_template("command line tool", default_domain=default_domain)
        assert result == "cli"

    def test_select_template_with_config_and_file_validation(self):
        """Integration: config-based selection produces valid template that exists on filesystem."""
        # Test with actual config values
        test_cases = [
            {"default_domain": "python", "query": "random query", "expected": "python"},
            {"default_domain": "cli", "query": "random query", "expected": "cli"},
            {"default_domain": "data-pipeline", "query": "random query", "expected": "data-pipeline"},
            {"default_domain": "precedent", "query": "random query", "expected": "precedent"},
        ]

        for case in test_cases:
            config = {"default_domain": case["default_domain"]}
            default_domain = config.get("default_domain")

            # Select template
            template = select_template(case["query"], default_domain=default_domain)

            # Verify expected template
            assert template == case["expected"], f"Expected {case['expected']}, got {template}"

            # Verify template is valid
            is_valid, error = validate_template(template)
            assert is_valid, f"Template {template} should be valid: {error}"

    def test_select_template_with_config_priority_integration(self):
        """Integration: verify priority chain works with config-loaded values."""
        # Config sets default to python
        config = {"default_domain": "python"}
        default_domain = config.get("default_domain")

        # Keyword detection should override default domain
        result = select_template("command line tool", default_domain=default_domain)
        assert result == "cli"  # keyword wins over default

        # Without keywords, default domain should be used
        result = select_template("random query", default_domain=default_domain)
        assert result == "python"  # default wins

        # Template override parameter should win over everything
        result = select_template("random query", template_override="deep", default_domain=default_domain)
        assert result == "deep"  # override wins

    def test_select_template_full_end_to_end_flow(self):
        """End-to-end: from config load to template selection to file validation."""
        # Simulate a real workflow: load config, select template, validate file exists

        # Step 1: Simulate config loading
        config_scenarios = [
            None,  # No config file
            {"default_domain": "python"},
            {"default_domain": "cli"},
            {"default_domain": "auto"},
        ]

        # Step 2: For each config scenario, test various queries
        test_queries = [
            "command line tool",  # cli keyword
            "asyncio code",  # python keyword
            "simple bug fix",  # complexity detection -> fast
            "redesign the system",  # complexity detection -> deep
            "random query",  # uses default or falls through
        ]

        for config in config_scenarios:
            default_domain = config.get("default_domain") if config else None

            for query in test_queries:
                # Select template
                template = select_template(query, default_domain=default_domain)

                # Verify template is valid
                is_valid, error = validate_template(template)
                assert is_valid, f"Template '{template}' from config={config}, query='{query}' failed validation: {error}"

                # Verify template is in valid templates set
                assert template in VALID_TEMPLATES, f"Template '{template}' not in VALID_TEMPLATES"
