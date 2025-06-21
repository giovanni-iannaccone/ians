package console

func FmtArray(array []string) string {
	var fmt string = "["

	for _, element := range array {
		fmt = fmt + "\"" + element + "\","
	}

	return fmt + "]"
}