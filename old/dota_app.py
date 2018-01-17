import urllib.request

from hero_cn_en import Hero

from old.html_parser import LocalHTMLParser

class DotaApp:

    hero_info = {}

    def __init__(self):
        html_parser = LocalHTMLParser()
	
        # Hero's name
        hero = "omniknight"

        # URL = "http://dotamax.com/hero/detail/" + hero + "/"
        URL = "http://dotamax.com/hero/detail/match_up_anti/" + hero + "/"

        print ("Sent HTTP Request...")
        page_source = urllib.request.urlopen(URL).read().decode()
        print ("Received HTTP Response...")
        print ("Processing information...")
        page_source = page_source.split("<tbody>")[1].split("</tbody>")[0]
        page_source = page_source.replace("%", "").replace("\n", "").replace("\r", "").replace("\t","").replace("<!--", "").replace("-->", "").replace(" ", "")
        html_parser.feed(page_source)

        for each in range(len(html_parser.hero)):
            DotaApp.hero_info[Hero.hero_name[html_parser.hero[each]]] = {"anti_index": html_parser.anti_index[each],
                                                                         "win_rate": html_parser.win_rate[each],
                                                                         "matches_played": html_parser.matches_played[each]}
        print (DotaApp.hero_info)

if __name__ == "__main__":
    DotaApp()
