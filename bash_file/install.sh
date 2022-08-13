blue="\e[34m"
green="\033[92m"
red="\e[1;31m"
yellow="\e[0;33m"

clear
echo "$blue ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ██╗███╗   ██╗ ██████╗          "
echo "$blue ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██║████╗  ██║██╔════╝          "
echo "$blue ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ██║██╔██╗ ██║██║  ███╗         "
echo "$blue ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██║██║╚██╗██║██║   ██║         "
echo "$blue ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗██║██║ ╚████║╚██████╔╝██╗██╗██╗"
echo "$blue ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝"

echo "\n"

#checking for python
echo  "$yellow [ * ] Checking for python"
which python > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
    echo "$green [ ✔ ]::[Python]: found"
    sleep 1
else
    echo "$red [ X ]::[Python]: python not found"
    sleep 1
    echo "$yellow [!]::[Installing Module Python...]"
    apt install python3
    apt install pip
    apt install pip2
    pip2 install --upgrade pip
fi

#installing requirements
echo "$yellow [ * ] Installing requirements"
pip install -r ../requirements.txt
echo "$blue [ ✔ ] Requirements installed"
sleep 1

echo "$blue Done, press ENTER to continue"
read

exit 0
fi