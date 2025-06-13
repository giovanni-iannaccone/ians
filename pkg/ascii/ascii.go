package ascii

import (
	"console"
)

func Main(version string) {
	console.Print(console.BoldGreen, mainBanner, version)
}

func PortScanner() {

}

func UserRecon() {
	console.Print(console.BoldBlue, userReconBanner)
}

func Warning() {
	console.Print(console.BoldRed, warningBanner)
}