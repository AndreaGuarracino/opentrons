# opentrons

As Python 3.10 currently does not allow for protocol simulation, it is recommended to use a version between 3.7.0 and 3.9.9.

For `Ubuntu 23.04`:

```shell
sudo apt-get update
sudo apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
tar -xf Python-3.9.0.tar.xz
cd Python-3.9.0
./configure --enable-optimizations
make -j `nproc`
sudo make altinstall

python3.9 --version
```

Install the Opentrons API:

```shell
mkdir -p ~/.venvs
python3.9 -m venv ~/.venvs/opentrons

~/.venvs/opentrons/bin/python3.9 -m pip install --upgrade opentrons
```

To simulate protocols:

```shell
opentrons_simulate my_protocol.py
```

To check the `Supported Protocol API Versions`:
- `./Opentrons-v7.0.2-linux-b36831.AppImage`
- click `Devices`
- select the robot (`OT-2 OT2CEP20221010R03`)
- click 3 points and then `Robot settings`
- click `Advanced`
- `Supported Protocol API Versions`: `v2.0 - v2.15`


# To do

- run a successful simulation
- human diluition test
- super-human diluition test
