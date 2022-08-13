blue="\e[34m"
clear

echo  "$blue  ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗██╗███╗   ██╗ ██████╗          "
echo  "$blue  ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝         "
echo  "$blue  ██║   ██║██████╔╝██║  ██║███████║   ██║   ██║██╔██╗ ██║██║  ███╗         "
echo  "$blue  ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██║██║╚██╗██║██║   ██║         "
echo  "$blue  ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝██╗██╗██╗"
echo  "$blue   ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝"

sudo chmod +x /etc/
sudo chmod +x /usr/share/doc
mv update.sh ..
cd ..
cd ..
sudo rm -rf ians
mkdir ians
cd ians
git clone https://github.com/giovanni-iannaccone/ians
sudo chmod +x bash_file/install.sh
echo -e "$blue Installing the newest version"
bash_file/install.sh
clear