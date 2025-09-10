package main

import (
	"fmt"
	"os"
	"time"

	"github.com/giovanni-iannaccone/ians/internal/bruteforce"
	"github.com/giovanni-iannaccone/ians/internal/chat"
	"github.com/giovanni-iannaccone/ians/internal/findConnected"
	"github.com/giovanni-iannaccone/ians/internal/portScanner"
	"github.com/giovanni-iannaccone/ians/internal/siteMapper"
	"github.com/giovanni-iannaccone/ians/internal/sniffer"
	"github.com/giovanni-iannaccone/ians/internal/trojanCreator"
	"github.com/giovanni-iannaccone/ians/internal/userRecon"

	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
	"github.com/giovanni-iannaccone/ians/pkg/system"
)

const VERSION = "2.0"

func exit() {
	console.Println(console.BoldRed, "Bye bye :)")
	os.Exit(0)
}

func handleOption(option uint) {
	switch option {
	case 1:
		portScanner.Initialize()
	
	case 2:
		sniffer.Initialize()

	case 3:
		bruteforce.Initialize()
	
	case 4:
		trojanCreator.Initialize()

	case 5:
		chat.Initialize()
	
	case 6:
		siteMapper.Initialize()
	
	case 7:
		userRecon.Initialize()

	case 8:
		findConnected.Initialize()
	
	case 9:
		printInfo()

	case 10:
		update()
	
	case 11:
		exit()

	default:
		
	}
}

func printInfo() {
	ascii.Info()

    console.Println(console.BoldBlue, "Author" + console.Reset + ": Giovanni Iannaccone")
    console.Println(console.BoldBlue, "Version" + console.Reset + ": %s", VERSION)
    console.Println(console.BoldRed, `
Tool written for educational purpose only, the user know what he is doing 
and the author is not responsible for any malicious tool of ians
`)

    console.Println(console.Red, "Press ENTER to continue ")
	fmt.Scanln()
}

func showOptions() {
	console.Println(console.BoldBlue, "[1]" + console.Reset + " Port scanner\tfor port scanning")
    console.Println(console.BoldBlue, "[2]" + console.Reset + " Sniffer\t\tfor sniffing ")
    console.Println(console.BoldBlue, "[3]" + console.Reset + " SSH Bruteforce\tbruteforce ssh credentials")
    console.Println(console.BoldBlue, "[4]" + console.Reset + " Trojan creator\tto create a trojan ")
    console.Println(console.BoldBlue, "[5]" + console.Reset + " Chat\t\tto create a private chat room ")
    console.Println(console.BoldBlue, "[6]" + console.Reset + " Site mapper\t\tbruteforce a site's directories")
    console.Println(console.BoldBlue, "[7]" + console.Reset + " User recon\t\tfind username on social")
    console.Println(console.BoldBlue, "[8]" + console.Reset + " Find\t\twho is connected to the router")

    console.Println(console.Reset, "\nNon hacking options:")
    console.Println(console.BoldBlue, "[9]" + console.Reset + " info\tinfo on the tool")
    console.Println(console.BoldBlue, "[10]" + console.Reset + " update\tupdate ians")
    console.Println(console.BoldBlue, "[11]" + console.Reset + " exit\tbye bye :(")
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
		console.Println(console.BoldRed, 	"    FOR EDUCATIONAL PURPOSE ONLY")
    	console.Println(console.BoldWhite, 	"    SELECT AN OPTION TO CONTINUE\n")
		showOptions()
		var option uint = takeOption()

		console.Clear()
		handleOption(option)
	}
}

