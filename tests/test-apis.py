"""
There's no obvious way to test the OAuth2 flow, so I just test
requests using an AccessToken I stole by hand.
Run with `pytest -s --pdb --disable-warnings`
"""

import requests, json
from http import HTTPStatus

access_token = 'V78Rmskep8yn6Jbrjt1Ue6qEOJbup7'
srv = 'https://localhost:8000'
temp_id = None

#
# CAMERAS endpoint
#
def test_list_cameras():
    response = requests.get(srv + '/cameras', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\n\ntest_list_cameras = {}'.format(json.loads(response.content)))


def test_list_cameras_filter():
    response = requests.get(srv + '/cameras?brand=go', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\n\ntest_list_cameras_filters = {}'.format(
        json.loads(response.content)))


def test_list_cameras_sort():
    response = requests.get(srv + '/cameras?sort=id&desc', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\n\ntest_list_cameras_sort = {}'.format(
        json.loads(response.content)))


def test_retrieve_camera():
    response = requests.get(srv + '/cameras/1', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\ntest_retrieve_camera = {}'.format(json.loads(response.content)))


def test_create_camera():
    global temp_id
    response = requests.post(srv + '/cameras/', headers={
        'Authorization': 'Bearer ' + access_token
    }, data={
        'camera_model': 'pippo', 'sensor_mp': 2, 'brand': 'pluto'
    }, verify=False)
    assert response.status_code == HTTPStatus.CREATED
    result = json.loads(response.content)
    temp_id = result['id']
    print('\ntest_create_camera = {}'.format(result))


def test_update_camera():
    global temp_id
    response = requests.put(
        srv + '/cameras/{}/'.format(temp_id), headers={
            'Authorization': 'Bearer ' + access_token
        }, data={
            'camera_model': 'pluto', 'sensor_mp': 2, 'brand': 'pippo'
        }, verify=False)
    assert response.status_code == HTTPStatus.OK
    result = json.loads(response.content)
    temp_id = result['id']
    print('\ntest_update_camera = {}'.format(result))


def test_partial_update_camera():
    global temp_id
    response = requests.patch(
        srv + '/cameras/{}/'.format(temp_id), headers={
            'Authorization': 'Bearer ' + access_token
        }, data={
            'sensor_mp': 4
        }, verify=False)
    assert response.status_code == HTTPStatus.OK
    result = json.loads(response.content)
    temp_id = result['id']
    print('\ntest_partial_update_camera = {}'.format(result))


def test_destroy_camera():
    global temp_id
    response = requests.delete(
        srv + '/cameras/{}/'.format(temp_id),
        headers={
            'Authorization': 'Bearer ' + access_token
        }, verify=False)
    assert response.status_code == HTTPStatus.NO_CONTENT
    print('\ntest_destroy_camera = {}'.format(response.status_code))

#
# DRONES endpoint
#


def test_list_drones():
    response = requests.get(srv + '/drones', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\n\ntest_list_drones = {}'.format(json.loads(response.content)))


def test_list_drones_filter():
    response = requests.get(srv + '/drones?serial_number=x6', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\n\ntest_list_drones_filters = {}'.format(
        json.loads(response.content)))


def test_list_drones_sort():
    response = requests.get(srv + '/drones?sort=id&desc', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\n\ntest_list_drones_sort = {}'.format(
        json.loads(response.content)))


def test_retrieve_drone():
    response = requests.get(srv + '/drones/1', headers={
        'Authorization': 'Bearer ' + access_token
    }, verify=False)
    assert response.status_code == HTTPStatus.OK
    print('\ntest_retrieve_drone = {}'.format(json.loads(response.content)))


def test_create_drone():
    global temp_id
    response = requests.post(srv + '/drones/', headers={
        'Authorization': 'Bearer ' + access_token
    }, data={
        'name': 'pippo', 'brand': 'pluto', 'serial_number': 'asdasdasd',
        'cameras': [1]
    }, verify=False)
    assert response.status_code == HTTPStatus.CREATED
    result = json.loads(response.content)
    temp_id = result['id']
    print('\ntest_create_drone = {}'.format(result))


def test_update_drone():
    global temp_id
    response = requests.put(
        srv + '/drones/{}/'.format(temp_id), headers={
            'Authorization': 'Bearer ' + access_token
        }, data={
            'name': 'pluto', 'brand': 'pippo', 'serial_number': 'asdasdasd',
            'cameras': [1]
        }, verify=False)
    assert response.status_code == HTTPStatus.OK
    result = json.loads(response.content)
    temp_id = result['id']
    print('\ntest_update_drone = {}'.format(result))


def test_partial_update_drone():
    global temp_id
    response = requests.patch(
        srv + '/drones/{}/'.format(temp_id), headers={
            'Authorization': 'Bearer ' + access_token
        }, data={
            'cameras': [1, 2]
        }, verify=False)
    assert response.status_code == HTTPStatus.OK
    result = json.loads(response.content)
    temp_id = result['id']
    print('\ntest_partial_update_drone = {}'.format(result))


def test_destroy_drone():
    global temp_id
    response = requests.delete(
        srv + '/drones/{}/'.format(temp_id),
        headers={
            'Authorization': 'Bearer ' + access_token
        }, verify=False)
    assert response.status_code == HTTPStatus.NO_CONTENT
    print('\ntest_destroy_drone = {}'.format(response.status_code))

