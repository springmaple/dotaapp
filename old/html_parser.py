from html.parser import HTMLParser

class LocalHTMLParser(HTMLParser):
        count = 0
        hero = []
        anti_index = []
        win_rate = []
        matches_played = []

        def handle_starttag(self, tag, attrs):
                pass

        def handle_endtag(self, tag):
                pass

        def handle_data(self, data):
                if LocalHTMLParser.count == 0:
                        LocalHTMLParser.hero.append(data)
                elif LocalHTMLParser.count == 1:
                        LocalHTMLParser.anti_index.append(data)
                elif LocalHTMLParser.count == 2:
                        LocalHTMLParser.win_rate.append(data)
                elif LocalHTMLParser.count == 3:
                        LocalHTMLParser.matches_played.append(data)

                LocalHTMLParser.count += 1
                LocalHTMLParser.count %= 4

        def handle_startendtag(self,tag,attrs):
                pass
