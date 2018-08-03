Vagrant.configure("2") do |config|


  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/trusty64"
    db.vm.hostname = "dbserver-clickhouse"
    db.vm.network "public_network", ip: "10.210.6.210"

    config.vm.provider "virtualbox" do |db|
      # Display the VirtualBox GUI when booting the machine
      db.name = "dbserver-clickhouse"
      db.cpus = 2
      db.memory = "3048"
    end      
  end

  config.vm.define "pg_db" do |pg_db|
    pg_db.vm.box = "centos/7"
    pg_db.vm.hostname = "dbserver-postgresql"
    pg_db.vm.network "public_network", ip: "10.210.6.211"
    pg_db.vm.synced_folder "E:\\VMs\\Share\\centos", "/home/share"  

    config.vm.provider "virtualbox" do |pg_db|
      # Display the VirtualBox GUI when booting the machine
      pg_db.name = "dwh-server"
      pg_db.cpus = 2
      pg_db.memory = "3048"

    end
  end
  
end