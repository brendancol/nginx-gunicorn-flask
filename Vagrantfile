# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # config.vm.box = "rsnhill/rhel-6.8.virtualbox.box"
  # config.vm.box_version = "14"
  config.vm.box = "iamseth/rhel-6.8-x86_64"
  config.vm.box_version = "1.0.0"
  config.vm.network "public_network",
    use_dhcp_assigned_default_route: true
  config.vm.synced_folder ".", "/opt/apps"
end


# anottations
# insert a routine to add python2.7 repository in rhel for puppet install it
