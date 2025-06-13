package main

import (
	"arpPoison"
	"bruteforce"
	"chat"
	"ddos"
	"portScanner"
	"siteMapper"
	"sniffer"
	"trojanCreator"
	"userRecon"

	"ascii"
	"console"
	"system"

	"fmt"
	"os"
	"time"
)

const VERSION = "2.0"

func exit() {
	console.Println(console.BoldRed, "Bye bye :)")
	os.Exit(0)
}

func findConnected() {

}

func handleOption(option uint) {
	switch option {
	case 1:
		portScanner.Initialize()
	
	case 2:
		sniffer.Initialize()

	case 3:
		ddos.Initialize()

	case 4:
		arpPoison.Initialize()

	case 5:
		bruteforce.Initialize()
	
	case 6:
		trojanCreator.Initialize()

	case 7:
		chat.Initialize()
	
	case 8:
		siteMapper.Initialize()

	case 9:
		findConnected()
	
	case 10:
		userRecon.Initialize()
	
	case 11:
		printInfo()

	case 12:
		update()
	
	case 13:
		exit()

	default:
		
	}
}

func printInfo() {

}

func showOptions() {
	console.Println(console.BoldBlue, "[1]" + console.Reset + " Port scanner\tfor port scanning")
    console.Println(console.BoldBlue, "[2]" + console.Reset + " Sniffer\t\tfor sniffing ")
    console.Println(console.BoldBlue, "[3]" + console.Reset + " DDos attack\t\tto start a DDos attack ")
    console.Println(console.BoldBlue, "[4]" + console.Reset + " Arp poison\t\tfor ARP poisoning")
    console.Println(console.BoldBlue, "[5]" + console.Reset + " Bruteforce\t\tfor bruteforce ")
    console.Println(console.BoldBlue, "[6]" + console.Reset + " Trojan creator\tto create a trojan ")
    console.Println(console.BoldBlue, "[7]" + console.Reset + " Chat\t\tto create a private chat room ")
    console.Println(console.BoldBlue, "[8]" + console.Reset + " Site mapper\t\tmap a site ")
    console.Println(console.BoldBlue, "[9]" + console.Reset + " Find\t\twho is connected to the router ")
    console.Println(console.BoldBlue, "[10]" + console.Reset + " User recon\t\tfind username on social")

    console.Println(console.Reset, "\nNon hacking options:")
    console.Println(console.BoldBlue, "[11]" + console.Reset + " info\tinfo on the tool")
    console.Println(console.BoldBlue, "[12]" + console.Reset + " update\tupdate ians")
    console.Println(console.BoldBlue, "[13]" + console.Reset + " exit\tbye bye :(")
}

func takeOption() uint {
	var option uint

	console.Print(console.White, "\n┌── [")
	console.Print(console.BoldGreen, "$ IANS $")
	console.Print(console.White, "] ── [")
	console.Print(console.BoldRed, "main")
	console.Print(console.White, "]:\n└───> ")

	fmt.Scanf("%d", &option)
	return option
}

func update() {
	system.Exec("chmod +x update.sh")
	system.Exec("./update.sh")
}

func main() {
	if system.Name == "windows" {
		console.Print(console.BoldRed, "You are using windows os, this can cause some problems")
        time.Sleep(time.Duration(2))
	} else {
		system.Exec("chmod +x setup.sh")
        if err := system.Exec("./setup.sh"); err != nil {
			console.Error(err.Error())
            os.Exit(1)
		}
	}

	console.Clear()
	ascii.Warning()
	fmt.Scanln()

	for {
		console.Clear()
		ascii.Main(VERSION)
		showOptions()
		var option uint = takeOption()

		console.Clear()
		handleOption(option)
	}
}

