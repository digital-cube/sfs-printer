# SFS-PRINTER


## setup printer on RPi-s:
```bash
apt install cups cups-bsd lynx
```
- download printer driver, for QL-700 from: 
- https://support.brother.com/g/b/downloadend.aspx?c=us&lang=en&prod=lpql700eus&os=10041&dlid=dlfp100459_000&flang=178&type3=10261
- turn on and connect the printer to RPi and install printer driver:
```bash
dpkg -i ql700pdrv-2.1.4-0.armhf.deb 
```
- restart cusp
```bash
service cups restart
```
- set default media size to 62mm(2.4") and save default options for the printer
- set QL-700 as default printer:
```bash
lpadmin -d QL-700
```

apt install git
git clone https://github.com/digital-cube/sfs-printer.git
cd sfs-printer
apt-get install python3-venv
python3 -m venv .venv


