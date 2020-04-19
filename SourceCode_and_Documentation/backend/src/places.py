import json, requests, datetime
from src.event import Event

URL = 'https://api.foursquare.com/v2/venues/search'
PREMIUM_URL = 'https://api.foursquare.com/v2/venues/'

# A dictionary containing the category id of all
# the required categories.
CATEGORIES = {
    '4bf58dd8d48988d1e1931735': 'arcade',
    '4bf58dd8d48988d116941735': 'bar',
    '4bf58dd8d48988d1e2941735': 'beach',
    '4bf58dd8d48988d16d941735': 'cafe',
    '4bf58dd8d48988d103951735': 'clothes',
    '4bf58dd8d48988d147941735': 'diner',
    '4d4b7105d754a06373d81259': 'events',
    '4bf58dd8d48988d18d941735': 'gaming-cafes',
    '4bf58dd8d48988d1f1931735': 'general-entertainment',
    '4bf58dd8d48988d175941735': 'gym',
    '5267e4d9e4b0ec79466e48c7': 'festival',
    '52e81612bcbc57f1066b7a0f': 'fishing-spot',
    '4bf58dd8d48988d17f941735': 'movie',
    '4bf58dd8d48988d181941735': 'museum',
    '52e81612bcbc57f1066b7a21': 'national-park',
    '4bf58dd8d48988d1f2931735': 'performing-arts',
    '507c8c4091d498d9fc8c67a9': 'public-art',
    '4bf58dd8d48988d125941735': 'tech-startup',
    '4bf58dd8d48988d193941735': 'water-park',
    '4bf58dd8d48988d17b941735': 'zoo'
    }   

# A dict containing all the relevant tags to the items in
# CATEGORIES dict.
CATEGORIES_TAGS = {
    'arcade': ['indoors', 'family-friendly', 'sporty'],
    'bar': ['romantic', 'indoors', 'hungry', 'artsy'],
    'beach': ['family-friendly', 'outdoors', 'sporty'],
    'cafe': ['romantic', 'indoors', 'hungry'],
    'clothes': ['indoors', 'family-friendly'],
    'diner': ['romantic', 'indoors', 'hungry', 'family-friendly'],
    'events': ['outdoors', 'artsy'],
    'gaming-cafes': ['indoors', 'sporty', 'geeky'],
    'general-entertainment': ['indoors', 'family-friendly'],
    'gym': ['indoors', 'sporty'],
    'festival': ['outdoors', 'family-friendly'],
    'fishing-spot': ['outdoors', 'family-friendly', 'sporty'],
    'movie': ['indoors', 'family-friendly'],
    'museum': ['indoors', 'geeky', 'artsy', 'historic', 'family-friendly'],
    'national-park': ['outdoors', 'family-friendly', 'sporty', 'historic'],
    'performing-arts': ['indoors', 'artsy', 'sporty', 'family-friendly'],
    'public-art': ['outdoors', 'artsy', 'family-friendly'],
    'tech-startup': ['indoors', 'geeky'],
    'water-park': ['outdoors', 'family-friendly', 'sporty'],
    'zoo': ['outdoors', 'family-friendly', 'geeky', 'historic']
    }


def get_all_events():
    event_list = []
    
    for category in CATEGORIES.keys():
        # params include ll as the latitude and longitude of the city or suburb to search in.
        client_info = {
            'client_id': 'DEPF4JDYDGBETTC5RDGFWUZTZIB2DDASK4XGU2H0POZSUGO0',
            'client_secret': 'XZP10N5EEDLDVNT04WPSFYUMWPX20LVCFGMC2JMWKXHRG2AI',
            'v': '20180604',
            'categoryId': category,
            'limit': 28,
            'radius': '100000',
            'll': '-33.8671417236, 151.2071075439'
            }

        response = requests.get(url=URL, params=client_info)
        data = json.loads(response.text)
        venues = data['response']['venues']

        for venue in venues:
            event_list.append(parseVenueToEvent(venue, category))

    return event_list


def get_event_details(id):
    premium_client_info = {
        'client_id': 'DEPF4JDYDGBETTC5RDGFWUZTZIB2DDASK4XGU2H0POZSUGO0',
        'client_secret': 'XZP10N5EEDLDVNT04WPSFYUMWPX20LVCFGMC2JMWKXHRG2AI',
        'v': '20180604'
        }
    call_url = PREMIUM_URL + id
            
    premium_response = requests.get(url=call_url, params=premium_client_info)
    premium_data = json.loads(premium_response.text)
            
    return premium_data['response']['venue']

def time_to_unix_time(time_str):
    if time_str == 'Midnight':
        dt = str(datetime.datetime.now()).split()[0] + ' ' + '00:00:00'
    else:
        if time_str[len(time_str)-2] == 'A':
            dt = datetime.datetime.strptime(time_str, '%H:%M AM')
        elif time_str[len(time_str)-2] == 'P':
            dt = datetime.datetime.strptime(time_str, '%H:%M PM')
        dt = str(datetime.datetime.now()).split()[0] + ' ' + str(dt).split()[1] 
    
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    return dt.timestamp()

def parseVenueToEvent(venue, category):
    time = ""
    start_time = 0
    end_time = 0
    url = ""
    description = ""
    # The four square API only has a price tier, so the price will remain an arbitrary value. 
    price = 0
    # The price_tier values are in the range (1-4) where '1' is for the pocket friendly places and '4' is for the most expensive places. 
    price_tier = 0
    is_online = True
    rating = 0
    image = ""
    
    if 'hours' in venue:
        time = venue['hours']['timeframes']
        line = str(time[0]['open'][0]['renderedTime'])
        line = line.split("–")
        start_time = time_to_unix_time(line[0])
        end_time = time_to_unix_time(line[1])
    if 'url' in venue:
        url = venue['url']
    if 'description' in venue:
        description = venue['description']
    if 'price' in venue:
        price_tier = venue['price']['tier']
    if 'photos' in venue:
        if 'groups' in venue['photos'] and len(venue['photos']['groups']) != 0:
            group = venue['photos']['groups'][0]
            if 'items' in group:
                item = group['items'][0]
                image = item['prefix'] + str(item['width']) + 'x' + str(item['height']) + item['suffix']
    if 'rating' in venue:
        rating = venue['rating']
    
    event_obj = Event(venue['id'], url,start_time, end_time, float(venue['location']['lat']), float(venue['location']
        ['lng']), venue['name'], "", price, is_online, description, "", CATEGORIES_TAGS.get(CATEGORIES.get(category)), price_tier, rating, image)
    
    return event_obj
