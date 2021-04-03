import httpx
import pytest


@pytest.mark.serial
def test_serve_localhost_http(ds_localhost_http_server):
    response = httpx.get("http://localhost:8041/_memory.json")
    assert {
        "database": "_memory",
        "path": "/_memory",
        "tables": [],
    }.items() <= response.json().items()


@pytest.mark.serial
def test_serve_localhost_https(ds_localhost_https_server):
    _, client_cert = ds_localhost_https_server
    response = httpx.get("https://localhost:8042/_memory.json", verify=client_cert)
    assert {
        "database": "_memory",
        "path": "/_memory",
        "tables": [],
    }.items() <= response.json().items()
