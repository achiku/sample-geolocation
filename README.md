sample-geolocation
==================

Sample setup for mysql/psgr geolocation setup using Ubuntu 13.10 on VirtualBox.

Requirements
------------

- Vagrant
- Packer
- Packer Template (https://github.com/shiguredo/packer-templates)
- VirtualBox


::
    
    $ git clone https://github.com/shiguredo/packer-templates
    $ cd packer-templates/ubuntu-13.10
    $ packer build -only=virtualbox-iso template.json


::

    $ vagrant box add geoloc ubuntu-13-10-x64-virtualbox.box


::
    
    $ git clone git@github.com:achiku/sample-geolocation.git
    $ cd sample-geolocation/mysql5.5
    $ vagrant provision


::
    
    $ mysql -u geoloc -h 192.168.33.58 -p  # password is geoloc

