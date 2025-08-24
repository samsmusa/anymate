import importlib

def get_routes_from_app(app_name: str):
    """
    Dynamically import <app_name>.routes and return CLIENT_ROUTE.
    """
    try:
        module = importlib.import_module(f"{app_name}.routes")
        return getattr(module, "CLIENT_ROUTE", [])
    except ModuleNotFoundError:
        return []
