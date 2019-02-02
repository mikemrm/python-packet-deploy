import os
import sys
import argparse
import requests
import textwrap
from .version import __version__
from .packet_api import PacketApi
from .print_functions import (
    print_devices,
    print_facilities,
    print_plans,
    print_operating_systems,
    print_capacity,
    print_errors
)


def parse_args(argv=None):
    default_host = os.environ.get('PACKET_HOST', 'https://api.packet.net')
    default_auth = os.environ.get('PACKET_AUTH')
    default_project = os.environ.get('PACKET_PROJECT')
    default_org = os.environ.get('PACKET_ORG')
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
            These Environment variables can be used instead of arguments:
              PACKET_HOST
              PACKET_AUTH
              PACKET_PROJECT
              PACKET_ORG
    '''))
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)

    api_group = parser.add_argument_group('API arguments')
    api_group.add_argument('--host', type=str, default=default_host,
                           help='packet.net api url. Default: https://api.packet.net')
    api_group.add_argument('--auth', type=str,
                           default=default_auth, help='API auth token [Required]')
    api_group.add_argument('--project', type=str,
                           default=default_project, help='Project id for associated devices [Required]')
    api_group.add_argument('--org', type=str,
                           default=default_org, help='Organization id for associated devices')

    parser.add_argument('command', type=str, choices=[
                        'list', 'capacity', 'power_up', 'power_down', 'reboot', 'add', 'remove'])

    add_group = parser.add_argument_group('add arguments')
    add_group.add_argument('--facility', type=str,
                           default=None, help='Facility code')
    add_group.add_argument('--plan', type=str, default=None, help='Plan slug')
    add_group.add_argument('--os', type=str, default=None,
                           help='Operating System slug')
    add_group.add_argument('--hostname', type=str, default='', help='Hostname')

    remove_group = parser.add_argument_group(
        'power_up/power_down/reboot/remove arguments')
    remove_group.add_argument('--device-id', type=str, default=None,
                              help='UUID of a device to be deleted')

    return parser.parse_args(argv)


class PacketDeployCommands(object):

    def __init__(self):
        self.args = parse_args()
        self.api = PacketApi(self.args.host, self.args.auth,
                             self.args.project, self.args.org)

    def run(self):
        try:
            return getattr(self, 'command_{}'.format(self.args.command.lower()))()
        except requests.exceptions.HTTPError as e:
            errors = e.response.json().get('errors', [])
            print_errors(errors)
        return 1

    def command_push(self):
        print_devices(self.api.getDevices(True))
        return 0

    def command_list(self):
        print_devices(self.api.getDevices(True))
        print_facilities(self.api.getFacilities())
        print_plans(self.api.getPlans())
        print_operating_systems(self.api.getOperatingSystems())
        return 0

    def command_add(self):
        new_device = {
            'plan': self.args.plan,
            'facility': self.args.facility,
            'operating_system': self.args.os,
            'hostname': self.args.hostname.strip()
        }

        plans = self.api.getPlans()
        if not new_device['plan']:
            print_plans(plans)
            new_device['plan'] = input('Enter plan slug: ')

        # Locate plan
        plan = None
        for p in plans:
            if p['slug'] == new_device['plan']:
                plan = p
                break
        else:
            print(new_device['plan'], 'not found')
            return 1

        if not new_device['facility']:
            # Only show facilities supporting selected plan
            facilities = [x for x in self.api.getFacilities() if plan['line']
                          in x['features']]
            print_facilities(facilities)
            new_device['facility'] = input('Enter facility code: ')

        if not new_device['operating_system']:
            # Only show os's available with selected plan
            operating_systems = [x for x in self.api.getOperatingSystems() if plan['slug'] in x[
                'provisionable_on']]
            print_operating_systems(operating_systems)
            new_device['operating_system'] = input(
                'Enter an operating system slug: ')

        if not new_device['hostname']:
            new_device['hostname'] = input('Enter a hostname: ').strip()
            if not new_device['hostname']:
                print('A hostname must be entered')
                return 1

        print('Creating device...')

        # Create device, exception is thrown if error occurs
        device = self.api.createDevice(**new_device)

        print('Created device:', device['hostname'], 'state:', device['state'])

        return 0

    def command_remove(self):
        i_device = self.args.device_id
        if not i_device:
            devices = self.api.getDevices(True)
            print_devices(devices)
            i_device = input('Specify the device UUID to be removed? ')

            # Verify device exists before attempting delete
            for device in devices:
                if device['id'] == i_device:
                    break
            else:
                print('Device not found')
                return 1
        self.api.deleteDevice(i_device)
        return 0

    def command_capacity(self):
        print_capacity(self.api.getCapacity())
        return 0

    def command_power_up(self):
        i_device = self.args.device_id
        if not i_device:
            devices = self.api.getDevices(True)
            print_devices(devices)
            i_device = input('Specify the device UUID to be removed? ')

            # Verify device exists before attempting delete
            for device in devices:
                if device['id'] == i_device:
                    break
            else:
                print('Device not found')
                return 1
        self.api.deviceAction(i_device, 'power_on')
        print('Device powered on')
        return 0

    def command_power_down(self):
        i_device = self.args.device_id
        if not i_device:
            devices = self.api.getDevices(True)
            print_devices(devices)
            i_device = input('Specify the device UUID to be removed? ')

            # Verify device exists before attempting delete
            for device in devices:
                if device['id'] == i_device:
                    break
            else:
                print('Device not found')
                return 1
        self.api.deviceAction(i_device, 'power_off')
        print('Device powered off')
        return 0

    def command_reboot(self):
        i_device = self.args.device_id
        if not i_device:
            devices = self.api.getDevices(True)
            print_devices(devices)
            i_device = input('Specify the device UUID to be removed? ')

            # Verify device exists before attempting delete
            for device in devices:
                if device['id'] == i_device:
                    break
            else:
                print('Device not found')
                return 1
        self.api.deviceAction(i_device, 'reboot')
        print('Device rebooted')
        return 0


def main():
    pd = PacketDeployCommands()
    return pd.run()

if __name__ == '__main__':
    sys.exit(main())
