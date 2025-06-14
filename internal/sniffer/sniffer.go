package sniffer

import (
	"ascii"
	"console"
	"system"

	"fmt"
)

func run(ip *string) error {
	return system.Exec("python3 internal/sniffer/sniffer.py " + *ip)
}

func Initialize() {
	var ip string
	ascii.Sniffer()
	console.Println(console.BoldRed, "\n\t\t     A simple sniffer\n")

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Type the address: ")
	fmt.Scanf("%s", &ip)

	if err := run(&ip); err != nil {
		console.Error("Error sniffing: %s", err.Error())
	}

	fmt.Scanln()
}