blue="\e[34m"
green="\033[92m"
red="\e[1;31m"
yellow="\e[0;33m"

clear
echo -e "$blue ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ██╗███╗   ██╗ ██████╗          "
echo -e "$blue ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██║████╗  ██║██╔════╝          "
echo -e "$blue ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ██║██╔██╗ ██║██║  ███╗         "
echo -e "$blue ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██║██║╚██╗██║██║   ██║         "
echo -e "$blue ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗██║██║ ╚████║╚██████╔╝██╗██╗██╗"
echo -e "$blue ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝"

echo

#checking for python
echo -e "$yellow [ * ] Checking for python"
which python > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
    echo -e "$green [ ✔ ]::[Python]: found"
    sleep 1
else
    echo -e "$red [ X ]::[Python]: python not found"
    sleep 1
    echo -e "$yellow [!]::[Installing Module Python...]"
    apt install python3
    apt install pip
    apt install pip2
    pip2 install --upgrade pip
fi

#installing requirements
echo -e "$yellow [ * ] Installing requirements"
pip install -r ../requirements.txt
echo -e "$blue [ ✔ ] Requirements installed"
sleep 1

echo -e "$blue Done, press ENTER to continue"
read

exit 0
fi
