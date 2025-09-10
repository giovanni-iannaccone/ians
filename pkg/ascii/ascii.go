package ascii

import (
	"github.com/giovanni-iannaccone/ians/pkg/console"
)

func Bruteforce() {
	console.Print(console.BoldBlue, bruteforceBanner)
}

func Chat() {
	console.Print(console.BoldYellow, chatBanner)
}

func FindConnected() {
	console.Print(console.BoldGreen, findConnectedBanner)
}

func Info() {
	console.Print(console.BoldWhite, infoBanner)
}

func Main(version string) {
	console.Print(console.BoldGreen, mainBanner, version)
}

func PortScanner() {
	console.Print(console.BoldBlue, portScannerBanner)
}

func SiteMapper() {
	console.Print(console.BoldBlue, siteMapperBanner)
}

func Sniffer() {
	console.Print(console.BoldRed, snifferBanner)
}

func TrojanCreator() {
	console.Print(console.BoldYellow, trojanCreatorBanner)
}

func UserRecon() {
	console.Print(console.BoldBlue, userReconBanner)
}

func Warning() {
	console.Print(console.BoldRed, warningBanner)
}