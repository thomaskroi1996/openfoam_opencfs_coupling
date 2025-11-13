# Install pip2
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python2 get-pip.py
# Install numpy
/home/openfoam/.local/bin/pip2 install numpy

# Delete install script
rm get-pip.py