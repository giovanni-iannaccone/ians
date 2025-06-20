package console

import (
	"bufio"
	"os"
)

func Scan(buffer *string) {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()

	*buffer = scanner.Text()
}