# sudo password: 'user'
sudo apt -y update
# Install pip2
#sudo apt install python-pip -y
# Install curl
sudo apt install curl -y

## Install openFoam
sudo apt-get -y update
# Install docker
curl -fsSL https://get.docker.com/ | sh
sudo usermod -aG docker user

# Now Log Out and Log In Again with your user

sudo sh -c "wget http://dl.openfoam.org/docker/openfoam8-linux -O /usr/bin/openfoam8-linux"
sudo chmod 755 /usr/bin/openfoam8-linux

echo "================================================================================"
echo "Installation process finished!"

# To complete the installation you need to Log Out and Log In Again with your user!
echo "To complete the installation you need to Log Out and Log In Again with your user!"

## Prepare openfoam
#openfoam8-linux
#sh PrepareOpenFoamContainer.sh