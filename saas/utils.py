import importlib

def get_routes_from_app(app_name: str, attrib="CLIENT_ROUTE", default=None):
    """
    """
    if default is None:
        default = []
    try:
        module = importlib.import_module(f"{app_name}.routes")
        return getattr(module, attrib, default)
    except ModuleNotFoundError:
        return []
