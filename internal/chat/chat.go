package chat 

import (
	"fmt"
	
	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
)

func clientChoice() {
	var ip string
	var port uint
	var nickname string

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Room's ip: ")
	fmt.Scanf("%s", &ip)

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Room's port: ")
	fmt.Scanf("%d", &port)

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Your nickname: ")
	fmt.Scanf("%s", &nickname)

	startClient(&ip, port, &nickname)
}

func serverChoice() {
	var ip string
	var port uint
	var pass string
	var passwd string = ""

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Your ip: ")
	fmt.Scanf("%d", &ip)

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Your port: ")
	fmt.Scanf("%d", &port)

	console.Print(console.Reset, "Do you want to set a password ? [y/n] ")
	fmt.Scanf("%s", pass)

	if pass == "y" || pass == "Y" {
		console.Print(console.BoldBlue, "[+] " + console.Reset + "Password: ")
		fmt.Scanf("%s", &passwd)
	}

	go startServer(ip, port, &passwd)
	startShell()
}

func Initialize() {
	var option uint
	ascii.Chat()

	console.Println(console.BoldBlue, "[1] " + console.Reset + "To host a room")
	console.Println(console.BoldBlue, "[2] " + console.Reset + "To enter a room")
	
	console.Print(console.Reset, "\n> ")
	fmt.Scanf("%d", &option)

	if option == 1 {
		serverChoice()
	} else {
		clientChoice()
	}
}