package jsonUtils

import (
	"encoding/json"
	"os"
)

func ExtractData(src string, dst *map[string]string) error {
	file, err := os.Open(src)
	if err != nil {
		return err
	}

	defer file.Close()

	decoder := json.NewDecoder(file)
	return decoder.Decode(dst)
}