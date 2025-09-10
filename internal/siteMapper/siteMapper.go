package siteMapper

import (
	"fmt"
	"net/http"
	"strings"
	
	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
	"github.com/giovanni-iannaccone/ians/pkg/files"
	"github.com/giovanni-iannaccone/ians/pkg/progressbar"
)

type submitFunction func(ch chan bool, prop properties, words *[]string)

type properties struct {
	extensions 	[]string
	target 		string
}

var STATUS_NOT_FOUND int = 404

func existsSubdir(ch chan bool, prop properties, word string) error {
	defer func() {
		ch <- true
	}()

	var url string = prop.target + word
	resp, err := http.Get(url)
	if err != nil {
		return err
	}

	if resp.StatusCode != STATUS_NOT_FOUND {
		console.Println(console.BoldGreen, "%s: %d" + strings.Repeat(" ", 50) + "\n", word, resp.StatusCode)
	}

	resp.Body.Close()
	return nil
}

func run(prop properties, words *[]string, submitTasks submitFunction) error {
	var totalWords uint = uint(len(*words) * len(prop.extensions))
	console.Println(console.Red, "%d words will be tryed", totalWords)

	ch := make(chan bool)
	go submitTasks(ch, prop, words)
	progressbar.DisplayProgressBar(totalWords, ch)

	return nil
}

func submitWords(ch chan bool, prop properties, words *[]string) {
	for _, word := range *words {
		for _, extension := range prop.extensions {
			go existsSubdir(
				ch,
				prop,
				word + extension,
			)
		}
	}
}

func takeExtensions() []string {
	var extensions = []string{"", ".bak", ".html", ".inc", ".js", ".orig", ".php"}

	var option string
	console.Println(console.BoldBlue, "This are the default extensions: %s", console.FmtArray(extensions))
	console.Print(console.Reset, "Do you want to use these ? [y/n] ")
	fmt.Scanf("%s", &option)

	if option != "y" && option != "Y" {
		var extensionsRaw string

		console.Print(console.BoldBlue, "[+] " + console.Reset + "Write your extensions separated by space: ")
		console.Scan(&extensionsRaw)
		extensions = strings.Split(extensionsRaw, " ")
	}

	return extensions
}

func Initialize() {
	ascii.SiteMapper()
	console.Println(console.BoldRed, "\t\tA site directories's bruteforce tool")

	var target string
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Type the target: ")
	fmt.Scanf("%s", &target)

	var extensions []string = takeExtensions()

	var path string
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the wordlist's path: ")
	fmt.Scanf("%s", &path)

	words := files.ReadLineByLine(path, true)

	console.Println(console.Red, "\nMapper is ready, press ENTER to start...")
	fmt.Scanln()

	err := run(properties{extensions, target}, &words, submitWords)
	if err != nil {
		console.Error(err.Error())
	}

	console.Println(console.Reset, "\n")
	fmt.Scanln()
}