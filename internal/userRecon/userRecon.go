package userRecon

import (
	"ascii"
	"console"

	"fmt"
	"net/http"
)

var socials = map[string]string{
	"About me": "https://about.me/%s",
	"Anime planet": "https://www.anime-planet.com/users/%s",
	"Badoo": "https://badoo.com/en/%s",
	"Blogger": "https://%s.blogspot.com",
	"Canva": "https://www.canva.com/%s",
	"CashMe": "https://cash.me/%s",
	"Chess": "https://www.chess.com/member/%s",
	"Codecademy": "https://codecademy.com/%s",
	"Deviantart": "https://%s.deviantart.com",
	"Disqus": "https://disqus.com/%s",
	"Duolingo": "https://www.duolingo.com/profile/%s?via=share_profile",
	"Ebay": "https://ebay.com/usr/%s",
	"Facebook": "https://facebook.com/%s",
	"Fotolog": "https://fotolog.com/%s",
	"Flickr": "https://flickr.com/people/%s",
	"Flipboard": "https://flipboard.com/@%s",
	"Github": "https://github.com/%s",
	"Google plus": "https://plus.google.com/+%s/posts",
	"Hacker news": "https://news.ycombinator.com/user?id=%s",
	"Instagram": "https://instagram.com/%s",
	"Linktree": "https://linktr.ee/%s",
	"Medium": "https://medium.com/@%s",
	"Minecrat": "https://playerdb.co/api/player/minecrat/%s",
	"Ngl": "https://ngl.link/%s",
	"Onlyfans": "https://onlyfans.com/%s",
	"Pastebin": "https://pastebin.com/u/%s",
	"Pinterest": "https://pinterest.com/%s",
	"Playstation network": "https://psnprofiles.com/%s",
	"Pornhub": "https://www.pornhub.com/users/%s",
	"Reddit": "https://reddit.com/user/%s",
	"Roblox": "https://roblox.com/user.aspx?username=%s",
	"Rumble": "https://rumble.com/user/%s",
	"Slack": "https://%s.slack.com",
	"Slideshare": "https://www.slideshare.net/%s",
	"Snapchat": "https://eelinsonice.appspot.com/web/deeplink/snapcode?username=%s&size=400&type=SVG",
	"Soundcloud": "https://soundcloud.com/%s",
	"Spotiy": "https://open.spotiy.com/user/%s",
	"Steam": "https://steamcommunity.com/id/%s",
	"Telegram": "https://t.me/%s",
	"Tiktok": "https://tiktok.com/@%s",
	"Tinder": "https://tinder.com/@%s",
	"Tumblr": "https://%s.tumblr.com",
	"Twitch": "https://twitch.tv/%s",
	"Vimeo": "https://vimeo.com/%s",
	"Wattpad": "https://www.wattpad.com/user/%s",
	"Wikipedia": "https://wikipedia.org/wiki/User:%s",
	"Wordpress profile": "https://profiles.wordpress.org/%s/",
	"Wordpress site": "https://wordpress.com/typo/?subdomain=%s",
	"X": "https://x.com/%s",
	"Xbox gamertag": "https://www.xboxgamertag.com/search/%s",
	"Xvideos": "https://www.xvideos.com/profiles/%s",
	"Youtube": "https://youtube.com/%s",
}

func check(username string) {
	for key, value := range socials {
		go func (key string, value string) {
			var url string = fmt.Sprintf(value, username)
			resp, _ := http.Get(url)

			if resp.StatusCode == 200 {
				console.Println(console.BoldGreen, "%s: found ✔", key)
			} else {
				console.Println(console.BoldRed, "%s: not found\t\t%d", key, resp.StatusCode)
			}
		}(key, value)
	}
}

func Initialize() {
	var username string

	ascii.UserRecon()
	console.Println(console.BoldRed, "  A username's finder across 46 social networks")

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the username you want to search: ")
	fmt.Scanf("%s", &username)

	check(username)
	fmt.Scanln()
}