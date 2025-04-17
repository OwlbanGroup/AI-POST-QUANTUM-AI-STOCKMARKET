import sys
try:
    import azure.storage.filedatalake
    import azure.ai.ml
    import azure.synapse.spark
    import delta.tables
    import powerbiclient
    print("All imports successful")
except ImportError as e:
    print(f"Import failed: {str(e)}")
    sys.exit(1)
