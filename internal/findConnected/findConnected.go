package findConnected

import (
	"errors"
	"fmt"
	"net"
	"os/exec"
	"strconv"
	
	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
)

func bruteforcePing(activeList *[]int, ip int, broadcast int) int {
	ch := make(chan int)

	submitTask(ch, ip, broadcast)

	var i int = 0
	var found int = 0
	for ip := range ch {
		if ip > 0 {
			*activeList = append(*activeList, ip)
			found++
		}

		i++

		if i >= broadcast-ip-1 {
			break
		}
	}

	return found
}

func format(mask string) string {
	var octets [4]int64 = [4]int64{0, 0, 0, 0}
	for i := 0; i < 4; i++ {
		octets[i], _ = strconv.ParseInt(mask[i*2:i*2+2], 16, 64)
	}

	return fmt.Sprintf("%d.%d.%d.%d", octets[0], octets[1], octets[2], octets[3])
}

func getBroadcast(ip int, cidr int) int {
	var b int = 0

	for i := cidr; i < 32; i++ {
		b = b*2 + 1
	}

	return ip | b
}

func getCidr(mask int) int {
	var i int

	for i = 32; i >= 0; i-- {
		if (mask & 1) != 0 {
			return i
		}

		mask >>= 1
	}

	return i
}

func getSubnetMask(iface string) (string, string, error) {
	mgmtInterface, err := net.InterfaceByName(iface)
	if err != nil {
		return "", "", errors.New("Unable to find interface")
	}
	addrs, err := mgmtInterface.Addrs()
	if err != nil {
		return "", "", err
	}

	for _, addr := range addrs {
		if ipnet, ok := addr.(*net.IPNet); ok {
			return ipnet.IP.String(), format(ipnet.Mask.String()), nil
		}
	}

	return "", "", errors.New("Unable to find subnet mask")
}

func int2ip(bits int) string {
	var octets [4]int = [4]int{0, 0, 0, 0}

	for i := 0; i < 4; i++ {
		octets[i] = bits & 0xFF
		bits >>= 8
	}

	return fmt.Sprintf("%d.%d.%d.%d", octets[3], octets[2], octets[1], octets[0])
}

func ip2int(ip string) int {
	var partial int = 0
	var sum int = 0

	for _, c := range ip {
		if c != '.' {
			partial = partial*10 + int(c) - '0'
		} else {
			sum = (sum << 8) + partial
			partial = 0
		}
	}

	return (sum << 8) + partial
}

func ping(ch chan int, ip int) {
	cmd := exec.Command("ping", "-c", "1", "-W", "10", int2ip(ip))
	_, err := cmd.CombinedOutput()

	if err != nil {
		ch <- -1
	} else {
		ch <- ip
	}
}

func submitTask(ch chan int, ip int, broadcast int) {
	for i := ip + 1; i < broadcast; i++ {
		go ping(ch, i)
	}
}

func Initialize() {
	ascii.FindConnected()
	console.Println(console.BoldRed, "Who is connected to your network ? ")

	ifaces, err := net.Interfaces()
	if err != nil {
		console.Fatal("%s", err.Error())
	}

	for _, iface := range ifaces {
		console.Print(console.Green, "\t%s", iface.Name)
	}

	var iface string
	console.Print(console.BoldBlue, "\n[+] "+console.Reset+"Enter your interface: ")
	fmt.Scanf("%s", &iface)

	ip, mask, err := getSubnetMask(iface)
	if err != nil {
		console.Fatal("%s", err.Error())
	}

	netIp := ip2int(ip) & ip2int(mask)
	cidr := getCidr(ip2int(mask))
	var broadcast int = getBroadcast(netIp, cidr)

	console.Println(console.Red, "\nScanner is ready, press ENTER to continue...")
	fmt.Scanln()

	var activeList []int
	n := bruteforcePing(&activeList, netIp, broadcast)

	for _, ip := range activeList {
		console.Print(console.Green, "%s\n", int2ip(ip))
	}

	if n != 0 {
		console.Println(console.BoldGreen, "\n\nFound %d devices", n)
	} else {
		console.Println(console.BoldRed, "\n\nNo device found...")
	}

	fmt.Scanln()
}
