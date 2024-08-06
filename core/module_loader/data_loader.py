def load_data_module_from_path(module_path: str):
    import importlib
    try:
        mod = importlib.import_module(module_path)
    except Exception as e:
        raise ImportError(f"Failed to import with module {module_path}")

    return mod