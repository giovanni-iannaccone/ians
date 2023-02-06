from rich.console import Console

import requests
import sys

class Check:
    
    def __init__(self, username):
        self.link = ""
        self.username = username

    def check(self, social):
        try:

            session = requests.Session()
            code = session.get(self.link).status_code

            if code == 200:
                console.print(f"{social}: found ✔", style="bold green")
            else:
                console.print(f"{social}: not found\t\t{code}", style="bold red")

            session.close()

        except:
            console.print(f"{social}: not found\t\t{code}", style="bold red")

    def aboutme(self):
        self.link = f"https://about.me/{self.username}"
        self.check("About me")

    def animeplanet(self):
        self.link = f"https://www.anime-planet.com/users/{self.username}"
        self.check("Anime planet")

    def badoo(self):
        self.link = f"https://badoo.com/en/{self.username}"
        self.check("Badoo")

    def blogger(self):
        if "." not in self.username:
            self.link = f"https://{self.username}.blogspot.com"
            self.check("Blogger")

    def canva(self):
        self.link = f"https://www.canva.com/{self.username}"
        self.check("Canva")

    def cashme(self):
        self.link = f"https://cash.me/{self.username}"
        self.check("CashMe")

    def chess(self):
        self.link = f"https://www.chess.com/member/{self.username}"
        self.check("Chess")

    def codecademy(self):
        self.link = f"https://codecademy.com/{self.username}"
        self.check("Codecademy")

    def deviantart(self):
        if "." not in self.username:
            self.link = f"https://{self.username}.deviantart.com"
            self.check("Deviantart")

    def disqus(self):
        self.link = f"https://disqus.com/{self.username}"
        self.check("Disqus")

    def duolingo(self):
        self.link = f"https://www.duolingo.com/profile/{self.username}?via=share_profile"
        self.check("Duolingo")

    def ebay(self):
        self.link = f"https://ebay.com/usr/{self.username}"
        self.check("Ebay")

    def facebook(self):
        self.link = f"https://facebook.com/{self.username}"
        self.check("Facebook")

    def fotolog(self):
        self.link = f"https://fotolog.com/{self.username}"
        self.check("Fotolog")

    def flickr(self):
        self.link = f"https://flickr.com/people/{self.username}"
        self.check("Flickr")

    def flipboard(self):
        self.link = f"https://flipboard.com/@{self.username}"
        self.check("Flipboard")

    def github(self):
        self.link = f"https://github.com/{self.username}"
        self.check("Github")

    def googleplus(self):
        self.link = f"https://plus.google.com/+{self.username}/posts"
        self.check("Google plus")

    def hackernews(self):
        self.link = f"https://news.ycombinator.com/user?id={self.username}"
        self.check("Hacker news")

    def instagram(self):
        self.link = f"https://instagram.com/{self.username}"
        self.check("Instagram")   

    def linktree(self):
        self.link = f"https://linktr.ee/{self.username}"
        self.check("Linktree")
    
    def medium(self):
        self.link = f"https://medium.com/@{self.username}"
        self.check("Medium")

    def minecraft(self):
        self.link = f"https://playerdb.co/api/player/minecraft/{self.username}"
        self.check("Minecraft")

    def ngl(self):
        self.link = f"https://ngl.link/{self.username}"
        self.check("Ngl")

    def onlyfans(self):
        self.link = f"https://onlyfans.com/{self.username}"
        self.check("Onlyfans")

    def pastebin(self):
        self.link = f"https://pastebin.com/u/{self.username}"
        self.check("Pastebin")

    def pinterest(self):
        self.link = f"https://pinterest.com/{self.username}"
        self.check("Pinterest")  

    def playstation_network(self):
        self.link = f"https://psnprofiles.com/{self.username}"
        self.check("Playstation network")

    def pornhub(self):
        self.link = f"https://www.pornhub.com/users/{self.username}"
        self.check("Pornhub")

    def reddit(self):
        self.link = f"https://reddit.com/user/{self.username}"
        self.check("Reddit")   

    def roblox(self):
        self.link = f"https://roblox.com/user.aspx?username={self.username}"
        self.check("Roblox")

    def rumble(self):
        self.link = f"https://rumble.com/user/{self.username}"
        self.check("Rumble")

    def slack(self):
        if "." not in self.username:
            self.link = f"https://{self.username}.slack.com"
            self.check("Slack")

    def slideshare(self):
        self.link = f"https://www.slideshare.net/{self.username}"
        self.check("Slideshare")

    def snapchat(self):
        self.link = f"https://feelinsonice.appspot.com/web/deeplink/snapcode?username={self.username}&size=400&type=SVG"
        self.check("Snapchat")

    def soundcloud(self):
        self.link = f"https://soundcloud.com/{self.username}"
        self.check("Sound cloud")
    
    def spotify(self):
        self.link = f"https://open.spotify.com/user/{self.username}"
        self.check("Spotify")

    def steam(self):
        self.link = f"https://steamcommunity.com/id/{self.username}"
        self.check("Steam")

    def telegram(self):
        self.link = f"https://t.me/{self.username}"
        self.check("Telegram")

    def tiktok(self):
        self.link = f"https://tiktok.com/@{self.username}"
        self.check("TikTok")

    def tinder(self):
        self.link = f"https://tinder.com/@{self.username}"
        self.check("Tinder")

    def tumblr(self):
        if "." not in self.username:
            self.link = f"https://{self.username}.tumblr.com"
            self.check("Tumblr")   

    def twitch(self):
        self.link = f"https://twitch.tv/{self.username}"
        self.check("Twitch")

    def twitter(self):
        self.link = f"https://twitter.com/{self.username}"
        self.check("Twitter")   

    def vimeo(self):
        self.link = f"https://vimeo.com/{self.username}"
        self.check("Vimeo")

    def wattpad(self):
        self.link = f"https://www.wattpad.com/user/{self.username}"
        self.check("Wattpad")

    def wikipedia(self):
        self.link = f"https://wikipedia.org/wiki/User:{self.username}"
        self.check("Wikipedia")

    def wordpress_profile(self):
        self.link = f"https://profiles.wordpress.org/{self.username}/"
        self.check("Wordpress profile")

    def wordpress_site(self):
        if "." not in self.username:
            self.link = f"https://{self.username}.wordpress.com"
            self.check("Wordpress site")

    def xboxgamertag(self):
        self.link = f"https://www.xboxgamertag.com/search/{self.username}"
        self.check("Xbox gamertag")

    def xvideos(self):
        self.link = f"https://www.xvideos.com/profiles/{self.username}"
        self.check("Xvideos")

    def youtube(self):
        self.link = f"https://youtube.com/{self.username}"
        self.check("Youtube")  

def checker(username):
    try:
        check = Check(username)

        check.aboutme()
        check.animeplanet()
        check.badoo()
        check.blogger()
        check.canva()
        check.cashme()
        check.chess()        
        check.codecademy()
        check.deviantart()
        check.disqus()
        check.duolingo()
        check.ebay()
        check.facebook()
        check.fotolog()
        check.flickr()
        check.flipboard()
        check.github()
        check.googleplus()
        check.hackernews()
        check.instagram()
        check.linktree()
        check.medium()
        check.minecraft()
        check.ngl()
        check.onlyfans()
        check.pastebin()
        check.pinterest()
        check.playstation_network()
        check.pornhub()
        check.reddit()
        check.roblox()
        check.rumble()
        check.slack()
        check.slideshare()
        check.soundcloud()
        check.snapchat()        
        check.spotify()
        check.steam()
        check.telegram()
        check.tiktok()
        check.tinder()
        check.tumblr()
        check.twitch()
        check.twitter()
        check.vimeo()
        check.wattpad()
        check.wikipedia()
        check.wordpress_profile()
        check.wordpress_site()
        check.xboxgamertag()
        check.xvideos()
        check.youtube()

    except Exception:
        exiting()

def allowed(username):
    allowed_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                    ".", "_", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    
    if not len(username):
        return False

    for char in username:
        if char not in allowed_char:
            return False

    return True

def exiting():
    console.print("\nExiting...", style="bold red")
    sys.exit()   

def initialize():
    try:
        global console
        console = Console()
        show_banner()
        console.print("  A username's finder across 46 social networks", style="bold red")

        username = console.input("\n[bold blue][+][/bold blue] Enter the username you want to search: ")

        while not allowed(username):
            console.print("Invalid username", style="italic yellow")
            username = console.input("\n[bold blue][+][/bold blue] Enter the username you want to search: ")
        print()

        checker(username)

    except KeyboardInterrupt:
        exiting()

    exiting()

def show_banner():
    banner = """
                  _nnnn_                      
                 dGGGGMMb     ,"""""""""""""".
                @p~qp~~qMb    | Linux Rules! |
                M|@||@) M|   _;..............'
                @,----.JM| -'
               JS^\__/  qKL
              dZP        qKRb
             dZP          qKKb
            fZP            SMMb
            HZM            MMMM
            FqM            MMMM
          __| ".        |\dS"qML
          |    `.       | `' \Zq
         _)      \.___.,|     .'
         \____   )MMMMMM|   .'
              `-'       `--' 
    
    """

    console.print(banner, style="bold blue")
