package progressbar

import (
	"strings"
	
	"github.com/giovanni-iannaccone/ians/pkg/console"
)

func DisplayProgressBar(max uint, ch chan bool) {
	const barMaxWidth uint = 38
	var loopIndex uint = 0

	for <- ch {
		loopIndex += 1

		var barWidth uint = barMaxWidth * loopIndex / max
		var bar string = strings.Repeat("▉", int(barWidth)) + strings.Repeat("-", int(barMaxWidth - barWidth))
		var progress float32 = float32(loopIndex) / float32(max) * 100

		console.Print(console.BoldBlue, "[%s] %.1f \r", bar, progress)

		if progress >= 100.0 {
			return
		}
	}
}