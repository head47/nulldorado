# EL DORA DO

## Setup

### Windows 10

1. Install Oracle VM VirtualBox
2. Request and load three files for VirtualBox (*.ova)
3. Import them into VirtualBox (just open using VirtualBox)
4. Setup NAT Network

    <img src="./static/teapot.png" width="10"/> File->Preferences->Network->Add new NAT Network

    <img src="./static/teapot.png" width="10"/> Double-click added NAT Network

    <img src="./static/teapot.png" width="10"/> Port Forwarding

    <img src="./static/teapot.png" width="10"/> Add six new port forwarding rules

5. Setup with following table

        | Name           | Protocol | Host IP | Host Port | Guest IP   | Guest Port |
        | :------------: | :------: | :-----: | :-------: | :--------: | :--------: |
        | node01_mariadb | TCP      |         | 13316     | 10.0.2.101 | 3306       |
        | node01_ssh     | TCP      |         | 1122      | 10.0.2.101 | 22         |
        | node02_mariadb | TCP      |         | 13326     | 10.0.2.102 | 3306       |
        | node02_ssh     | TCP      |         | 1222      | 10.0.2.102 | 22         |
        | node03_mariadb | TCP      |         | 13336     | 10.0.2.103 | 3306       |
        | node03_ssh     | TCP      |         | 1322      | 10.0.2.103 | 22         |


6. Change node 3 MAC address (or node 2, or node 1, idk I'm not a programmer)


