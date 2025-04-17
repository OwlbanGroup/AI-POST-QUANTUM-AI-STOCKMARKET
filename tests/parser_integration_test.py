"""Comprehensive test for FabricDataParser."""
import json
from src.data.fabric_data_parser_new import FabricDataParser

def run_tests():
    results = {
        'initialization': test_initialization(),
        'dependencies': test_dependencies(),
        'services': test_services()
    }
    with open('tests/parser_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    return results

def test_initialization():
    try:
        parser = FabricDataParser('test', 'test')
        return {'status': 'success', 'credential': parser.credential is not None}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}

def test_dependencies():
    from src.data.fabric_data_parser_new import AZURE_DEPS_AVAILABLE, DEPENDENCY_WARNINGS
    return {
        'azure_available': AZURE_DEPS_AVAILABLE,
        'warnings': DEPENDENCY_WARNINGS
    }

def test_services():
    parser = FabricDataParser('test', 'test')
    return {
        'storage': bool(parser.storage_client),
        'ml': bool(parser.ml_client),
        'synapse': bool(parser.synapse_client)
    }

if __name__ == '__main__':
    results = run_tests()
    print(json.dumps(results, indent=2))
