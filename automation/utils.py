import requests
from django.conf import settings

HEADERS = {
    "Content-Type": "application/json",
    settings.AUTOMATE_SERVICE_HEADER_KEY: settings.AUTOMATE_SERVICE_API_KEY
}
AUTOMATE_SERVICE_URL = settings.AUTOMATION_API_BASE


def create_workflow(workflow_data: dict) -> dict:
    """Create a workflow in automation and return the JSON response."""
    url = f"{AUTOMATE_SERVICE_URL}/workflows"
    resp = requests.post(url, json=workflow_data, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def update_workflow(workflow_id: str, workflow_data: dict) -> dict:
    """Update an existing workflow in automation."""
    url = f"{AUTOMATE_SERVICE_URL}/workflows/{workflow_id}"
    resp = requests.patch(url, json=workflow_data, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def active_workflow(workflow_id: str) -> dict:
    """Update an existing workflow in automation."""
    url = f"{AUTOMATE_SERVICE_URL}/workflows/{workflow_id}/activate"
    resp = requests.post(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def deactivate_workflow(workflow_id: str) -> dict:
    """Update an existing workflow in automation."""
    url = f"{AUTOMATE_SERVICE_URL}/workflows/{workflow_id}/deactivate"
    resp = requests.post(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def delete_workflow(workflow_id: str) -> None:
    """Delete a workflow from automation."""
    url = f"{AUTOMATE_SERVICE_URL}/workflows/{workflow_id}"
    resp = requests.delete(url, headers=HEADERS, timeout=10)
    if resp.status_code not in (200, 204):
        resp.raise_for_status()
