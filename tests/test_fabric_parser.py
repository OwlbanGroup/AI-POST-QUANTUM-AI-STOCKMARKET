"""Test script for FabricDataParser."""
import pytest
from src.data.fabric_data_parser_new import FabricDataParser, AZURE_DEPS_AVAILABLE, DEPENDENCY_WARNINGS

def test_parser_initialization():
    """Test basic parser initialization."""
    parser = FabricDataParser("test_workspace", "test_lakehouse")
    assert parser.workspace_id == "test_workspace"
    assert parser.lakehouse_id == "test_lakehouse"
    print("Basic initialization test passed")

def test_azure_dependencies():
    """Verify Azure dependency status."""
    print(f"Azure dependencies available: {AZURE_DEPS_AVAILABLE}")
    if DEPENDENCY_WARNINGS:
        print("Dependency warnings:")
        for warning in DEPENDENCY_WARNINGS:
            print(f"- {warning}")

def test_fallback_behavior():
    """Test fallback behavior when Azure services are unavailable."""
    parser = FabricDataParser("test", "test")
    if not AZURE_DEPS_AVAILABLE:
        assert parser.storage_client is None
        assert parser.ml_client is None
        assert parser.synapse_client is None
        print("Fallback behavior working as expected")

if __name__ == "__main__":
    test_parser_initialization()
    test_azure_dependencies()
    test_fallback_behavior()
    print("All tests completed")
