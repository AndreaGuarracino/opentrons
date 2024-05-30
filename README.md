# opentrons

## Opentron App

Donwload it from https://opentrons.com/ot-app/.

## Protocol simulator

### Python issue

#### 2023/12/07

As Python 3.10 currently does not allow for protocol simulation (https://support.opentrons.com/s/article/Simulating-OT-2-protocols-on-your-computer), it is recommended to use a version between 3.7.0 and 3.9.9.

For `Ubuntu 23.04`:

```shell
sudo apt-get update
sudo apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

cd ~
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
tar -xf Python-3.9.0.tar.xz
cd Python-3.9.0
./configure --enable-optimizations
make -j `nproc`
sudo make altinstall

python3.9 --version
```

#### 2024/04/24

With Python 3.9, I get an import error related to the `ParamSpec` type hint from the `typing` module. This error occurs because `ParamSpec` was introduced in Python 3.10.

For `Ubuntu 23.10`:

```shell
sudo apt-get update
sudo apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

cd ~
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz
tar -xf Python-3.10.0.tar.xz
cd Python-3.10.0
./configure --enable-optimizations
make -j `nproc`
sudo make altinstall

python3.10 --version
```


### API

Install the Opentrons API:

```shell
mkdir -p ~/.venvs
python3.10 -m venv ~/.venvs/opentrons

~/.venvs/opentrons/bin/python3.10 -m pip install --upgrade opentrons
```

To simulate protocols:

```shell
source /home/guarracino/.venvs/opentrons/bin/activate
opentrons_simulate my_protocol.py
```

To check the `Supported Protocol API Versions`:
- `./Opentrons-v7.3.0-linux-b43335.AppImage`
- click `Devices`
- select the robot (`OT-2 OT2CEP20221010R03`)
- click 3 points and then `Robot settings`
- click `Advanced`
- `Supported Protocol API Versions`: `v2.0 - v2.17`
