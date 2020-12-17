# EL DORA DO

## Setup

### Windows 10

1. Install Oracle VM VirtualBox
2. Request and load three files for VirtualBox (*.ova)
3. Import them into VirtualBox (just open using VirtualBox)
    
    If you have some troubles with importing ova into VirtualBox, try to execute from VirtualBox installation directory:

    > ```vboxmanage import "path\to\ova\node01.ova"```

    > ```vboxmanage import "path\to\ova\node02.ova"```

    > ```vboxmanage import "path\to\ova\node03.ova"```

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

7. Create file `secret` in project root directory and fill it how you want, but don't leave it empty

8. Run all (three) virtual systems from VirtualBox

9. If they are not loading, put in EFI shell:
    > ```fs0:\EFI\arch\grubx64.efi```

10. Log into the system using login: `user` and password `Lower829-nature--`

11. If you want to change password write `passwd` and follow instructions

12. After log into the system write the following line to boot linux automaticly
    > `sudo grub-install --target=x86_64-efi --efi-directory=/efi` 
    
13. Then you need to shutdown all nodes, and remember, which was shutdowned the lastest

14. Boot them again, and in the last shutdowned system write
    > `sudo galera_new_cluster`

    in others write
    > `sudo systemctl start mysqld`

15. On your host system:

    1. Setup python
    2. Setup pip
    3. Setup django
    4. Setup mysqlclient
    5. Resolve warnings with environment variables (especially PATH)
    6. Run from project root directory
        > `python manage.py runserver`

16. After all these steps are taken, you can obtain access to localhost:8000 (maybe not 8000), so open it in web browser.