#!/usr/bin/env python3

import sys
from pathlib import Path, PurePath
from cloudbridge.cloud.factory import CloudProviderFactory, ProviderList


config = {'os_username': '',
          'os_password': '',
          'os_auth_url': 'http://cardiff.climb.ac.uk:5000/v3',
          'os_project_name': '',
          'os_user_domain_name': '',
          'os_project_domain_name': '',
          }

if config['os_password']:
    print('Using config from script')
    try:
        provider = CloudProviderFactory().create_provider(ProviderList.OPENSTACK, config)
    except:
        print('Cannot connect to cloud provider with supplied config')
elif Path((str(PurePath.joinpath(Path.home(), '.cloudbridge')))).exists():
    print('Using config from ' + str(Path.home()) + '/.cloudbridge')
    try:
        provider = CloudProviderFactory().create_provider(ProviderList.OPENSTACK, {})
    except:
        print('Cannot connect to cloud provider with supplied config')
elif Path('/etc/cloudbridge.ini').exists():
    print('Using config from /etc/cloudbridge.ini')
    try:
        provider = CloudProviderFactory().create_provider(ProviderList.OPENSTACK, {})
    except:
        print('Cannot connect to cloud provider with supplied config')
else:
    print('Please supply a provider configuration files')


OS = ['CentOS']

selectedImages = []

print('Finding images...')
for os in OS:
    imageList = [i for i in provider.compute.images.list()
        if os.lower() in i.name.lower()]
    
    if len(imageList) > 0:
        selectedImages.append(imageList[0])

    no = str(len(imageList))
    print('Found ' + no + ' ' + os + ' images')
    
    for i in imageList:
        print('Name: ' + i.name + '\t ID: ' + i.id)

for i in selectedImages:
    print('Selected image ' + i.name + ' with ID: ' + i.id)


selectedFlavours = []

print('Finding flavours...')
flavourList = sorted([f for f in provider.compute.instance_types.list()
                    if 'tiny' in f.name.lower() and f.vcpus >= 1 and f.ram >= 1],
                    key=lambda x: x.vcpus)

no = str(len(flavourList))
print('Found ' + no + ' flavours')

for f in flavourList:
    print('Name: ' + f.name + 
            '\t ID: ' + f.id + 
            '\t vCPUS: ' + str(f.vcpus) + 
            '\t RAM: ' + str(f.ram/1024) + ' GB')

if len(flavourList) > 0:
    selectedFlavours.append(flavourList[0])
    print('Selected flavour ' + flavourList[0].name + ' with ID: ' + flavourList[0].id)

keyList = provider.security.key_pairs.find('sbi6mjb_decode')
netList = provider.network.subnets.list()

img = selectedImages[0]
inst_type = flavourList[0]
net = netList[0]
key = keyList[0]

if len(sys.argv) > 1:
    for i in range(1):
        instName = "CloudBridge-intro" + str(i)
        print('Creating instance: ' + instName)
        lc = provider.compute.instances.create_launch_config()
        lc.add_volume_device(source=img, size=120, is_root=True)
        inst = provider.compute.instances.create(name=instName, 
                image=img, 
                instance_type=inst_type, 
                key_pair=key, 
                subnet=net, 
                launch_config=lc)
        inst.wait_till_ready()
        ip = inst.public_ips[0]
        print(instName + ' [' + str(ip) + '] ' + inst.state)
