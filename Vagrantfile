# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "iamseth/rhel-6.8-x86_64"
  config.vm.box_version = "1.0.0"
  config.vm.synced_folder ".", "/opt/apps"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision "shell", path: "install.sh"
end
