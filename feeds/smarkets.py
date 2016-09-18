def setup_connection():
    pass


def get_xml():
    import requests
    base_url = 'http://odds.smarkets.com/oddsfeed.xml'
    r = requests.get(base_url)
    return r.text


def parse_xml(xml):
    import xmltodict
    midpoint = xmltodict.parse(xml, process_namespaces=True)
    return midpoint['odds']['event']


def get_relevant_matches(eventlist):
    from feeds.config import PICK_LIST
    return [match for match in eventlist if match["@parent_slug"] in PICK_LIST]


def parse_match(match):
    from datetime import datetime
    from core.models import Match
    date = match['@date']
    home_team, away_team = match['@name'].split(" vs. ")
    data_dict = {"match_date": (datetime.strptime((match['@date']+" "+match['@time']), "%Y-%m-%d %H:%M:%S")),
     "league": match['@parent_slug'],
    "home_team": home_team,
    "away_team": away_team}
    m = Match(**data_dict)
    return m

def run_all():
    matches = get_relevant_matches(parse_xml(get_xml()))
    for thing in matches: print parse_match(thing)
    yield


class Bet(object):
    #creates a Bet object from the parsed XML using whatever is there
    #should not be used with a contract entry item still in.
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            print initial_data
            for key in dictionary:
                setattr(self, key.strip('@'), dictionary[key])
        for key in kwargs:
            setattr(self, key.strip('@'), kwargs[key])
        self.price = initial_data["contract"][0]["bids"]['price'][2]["@decimal"]


class Contract(object):
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key.strip('@'), dictionary[key])
        for key in kwargs:
            setattr(self, key.strip('@'), kwargs[key])
    #use the sublist to create secondary attributes, or go more granular but more objects?


def parse_prices(contract_entry):
    return None


def parse_contracts(market_item):
from core.models import Odds
#each market potentially many
bet_name = market_item["@slug"]
print bet_name
for item in market_item["contract"]:
    if item["bids"]:
        bid_offer="bids"
    elif item["offers"]:
        bid_offer="offers"
    data_dict = {"bet_name": bet_name,
        "bet_type": item["@slug"],
        "price": item[bid_offer]["price"][0]["@decimal"],
        "bid_offer": bid_offer}

    current_bet = Odds(**data_dict
        )
        print current_bet


def parse_market_list(list_of_markets):
    useful_markets = [market for market in list_of_markets if len(market) == 4]
    return useful_markets



"""

Market - list of items (bet entries) containing
Bet entry
    - @id
    - @slug (e.g. the bet name)
    - @winners (irrelevant in football, i believe)
    - contract (can be blank if not offered)

contract - list of items containing
    - @id
    - @name
    - @slug
    - bids

bids - list of items containing
    - @id
    - @name
    - @slug
    -price

price - list of items containing
    @decimal
    @percent
    @backers_stake
    @liability



So bet info  =
bet_entry.@id
bet_entry.@slug
bet_entry["contract"][0]["bids"]["price"][0]["@decimal"]
timestamp = now()

def output_lines(matches):
    for match in matches:
        for market in match["market"]:
            try:
                if len(market)==4:
                    for contract in market['contract']:
                        print "MAIN"
                        print datetime.strptime((match['@date']+" "+match['@time']), "%Y-%m-%d %H:%M:%S"),
                        print match["@parent_slug"],
                        print match["@name"].split(" vs. "),
                        print market["@slug"] + ":" +contract["@slug"],
                        print contract["bids"]["price"][0]["@decimal"]
                else:
                    pass
            except IndexError, KeyError:
                print "Index/KeyError"
                print datetime.strptime((match['@date']+" "+match['@time']), "%Y-%m-%d %H:%M:%S"),
                print match["@parent_slug"],
                print match["@name"].split(" vs. "),
                print market["@slug"],
                print market['contract']
            except TypeError, e:
                print "TypeError", e
                print datetime.strptime((match['@date']+" "+match['@time']), "%Y-%m-%d %H:%M:%S"),
                print match["@parent_slug"],
                print match["@name"].split(" vs. "),
                print market["@slug"]

except IndexError:
    print
for thing in market:
   if len(thing==4):

"""