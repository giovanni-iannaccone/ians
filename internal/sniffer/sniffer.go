package sniffer

import (
	"fmt"

	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
	"github.com/giovanni-iannaccone/ians/pkg/system"
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