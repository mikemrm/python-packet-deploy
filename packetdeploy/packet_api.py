import requests
import json
from .version import __version__

URL_PROJECT = '/projects/{project_id}'
URL_ORGANIZATION = '/organizations/{org_id}'
CAPACITY_PATH = '/capacity'
FACILITIES_PATH = '/facilities'
PLANS_PATH = '/plans'
OPERATING_SYSTEMS_PATH = '/operating-systems'
DEVICES_PATH = '/devices'
DEVICE_PATH = DEVICES_PATH + '/{device_id}'
DEVICE_ACTION_PATH = DEVICE_PATH + '/actions'


class PacketApi(object):

    def __init__(self, url, auth, project, organization=None):
        self.url = url.strip('/ ')
        self.project = project and project.strip() or None
        self.organization = organization and organization.strip() or None
        if not self.project:
            raise RuntimeError('Project ID must be provided')
        self.session = requests.Session()
        if not auth.strip():
            raise RuntimeError('No auth token provided to PacketApi')
        self.session.headers[
            'User-Agent'] = 'packetdeploy/{}'.format(__version__)
        self.session.headers['X-Auth-Token'] = auth

    def getUrl(self, path, **kwargs):
        return self.url + path.format(**kwargs)

    def getProjectUrl(self, path, **kwargs):
        return self.getUrl(URL_PROJECT.format(project_id=self.project) + path, **kwargs)

    def getOrganizationUrl(self, path, **kwargs):
        return self.getUrl((self.organization and URL_ORGANIZATION.format(org_id=self.organization) or '') + path, **kwargs)

    def getProjectOrOrgUrl(self, path, **kwargs):
        if self.project:
            return self.getProjectUrl(path, **kwargs)
        return self.getOrganizationUrl(path, **kwargs)

    def getCapacity(self):
        response = self.session.get(self.getProjectUrl(CAPACITY_PATH))
        response.raise_for_status()
        return response.json()['capacity']

    def getFacilities(self):
        response = self.session.get(self.getProjectUrl(FACILITIES_PATH))
        response.raise_for_status()
        return response.json()['facilities']

    def getPlans(self):
        response = self.session.get(self.getProjectUrl(PLANS_PATH))
        response.raise_for_status()
        return response.json()['plans']

    def getOperatingSystems(self):
        response = self.session.get(self.getUrl(OPERATING_SYSTEMS_PATH))
        response.raise_for_status()
        return response.json()['operating_systems']

    def getDevices(self, fetch_all=False):
        response = self.session.get(self.getProjectOrOrgUrl(DEVICES_PATH))
        response.raise_for_status()
        if not fetch_all:
            return response.json()['devices']
        data = response.json()
        devices = data['devices']
        while data['meta']['current_page'] < data['meta']['last_page']:
            response = self.session.get(self.getProjectOrOrgUrl(DEVICES_PATH), params={
                                        'page': data['meta']['current_page'] + 1})
            response.raise_for_status()
            data = response.json()
            devices += data['devices']
        return devices

    def createDevice(self, **device):
        if 'facility' not in device:
            device['facility'] = 'any'
            #raise RuntimeError('New device must have "facility" defined')
        if 'plan' not in device:
            raise RuntimeError('New device must have "plan" defined')
        if 'operating_system' not in device:
            raise RuntimeError(
                'New device must have "operating_system" defined')
        response = self.session.post(
            self.getProjectUrl(DEVICES_PATH), json=device)
        response.raise_for_status()
        return response.json()

    def getDevice(self, device_id):
        response = self.session.get(
            self.getUrl(DEVICE_PATH, device_id=device_id))
        response.raise_for_status()
        return response.json()['device']

    def updateDevice(self, device_id, **device_updates):
        response = self.session.put(self.getUrl(
            DEVICE_PATH, device_id=device_id), json=device_updates)
        response.raise_for_status()
        return True

    def deleteDevice(self, device_id, force_delete=False):
        response = self.session.delete(self.getUrl(
            DEVICE_PATH, device_id=device_id), params={'force_delete': force_delete})
        response.raise_for_status()
        return True

    def deviceAction(self, device_id, Type):
        response = self.session.post(self.getUrl(
            DEVICE_ACTION_PATH, device_id=device_id), params={'type': Type})
        response.raise_for_status()
        return True
