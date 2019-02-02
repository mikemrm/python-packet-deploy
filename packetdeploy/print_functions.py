def print_devices(devices):
    print('Devices:')
    for device in sorted(devices, key=lambda x: x['hostname']):
        print('  {id}: {hostname} State: {state}'.format(**device))
    if not devices:
        print('  No devices')


def print_facilities(facilities):
    print('Facilities:')
    for facility in sorted(facilities, key=lambda x: x['name']):
        print('  {name} (code: {code})'.format(**facility))
    if not facilities:
        print('  No facilities')


def print_plans(plans):
    print('Plans:')
    for plan in sorted(plans, key=lambda x: x['name']):
        print('  {name} (slug: {slug})'.format(**plan))
    if not plans:
        print('  No plans')


def print_operating_systems(operating_systems):
    print('Operating Systems:')
    for os in sorted(operating_systems, key=lambda x: x['name']):
        print('  {name} (slug: {slug})'.format(**os))
    if not operating_systems:
        print('  No operating systems')


def print_capacity(capacity):
    print('Capacity:')
    for facility in sorted(capacity.keys()):
        print('  Facility:', facility)
        for plan in sorted(capacity[facility].keys()):
            c = capacity[facility][plan]
            print(f'    {plan}:')
            print('      State:', c['level'])
            print('      Servers:', c['servers'])


def print_errors(errors):
    print('({:d}) Errors:'.format(len(errors)))
    for error in errors:
        print(' ', error)
    if not errors:
        print('  None')
