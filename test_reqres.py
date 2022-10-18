import requests
from pytest_voluptuous import S
from voluptuous import Schema, PREVENT_EXTRA, Optional

create_user_schema = Schema(
    {
        "data": {
            "id": int,
            "email": str,
            "first_name": str,
            "last_name": str,
            "avatar": str
        },
        "support": {
            "url": str,
            "text": str
        }
    },
    extra=PREVENT_EXTRA,
    required=True,
)

create_and_update_user_schema = Schema(
    {
        "name": str,
        "job": str,
        Optional("id"): str,
        "updatedAt": str
    },
    extra=PREVENT_EXTRA,
    required=True,
)


def test_get_single_user():
    result = requests.get("https://reqres.in/api/users/2")

    assert result.status_code == 200
    assert result.json() == S(create_user_schema)
    assert len(result.json()['data']) != 0
    assert len(result.json()['support']) != 0
    assert result.json()['data']['first_name'] == 'Janet'


def test_create_user():
    name = 'morpheus'
    job = 'zion resident'

    result = requests.put(
        "https://reqres.in/api/users/2",
        json={'name': name, 'job': job}
    )

    assert result.status_code == 200
    assert result.json() == S(create_and_update_user_schema)
    assert result.json()["name"] == name
    assert result.json()["job"] == job


def test_update_user():
    result = requests.patch(
        "https://reqres.in/api/users/2",
        json={'name': 'morpheus', 'job': 'zion resident'}
    )

    assert result.status_code == 200
    assert result.json() == S(create_and_update_user_schema)
    assert result.json()['name'] == 'morpheus'
    assert result.json()['job'] == 'zion resident'


def test_register_successful():
    email = 'eve.holt@reqres.in'
    password = 'pistol'

    result = requests.post(
        "https://reqres.in/api/register",
        json={'email': email, 'password': password}
    )

    assert result.status_code == 200
    assert result.json()['id'] == 4
    assert result.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_register_unsuccessful():
    result = requests.post(
        "https://reqres.in/api/register",
        json={"email": "sydney@fife"}
    )

    assert result.status_code == 400
    assert result.json()['error'] == 'Missing password'


def test_delete_user():
    result = requests.delete("https://reqres.in/api/users/2")

    assert result.status_code == 204
