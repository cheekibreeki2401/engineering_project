from bs4 import BeautifulSoup as bs
import requests

# defining the user-agent and language
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

LANGUAGE = "en-US,en;q=0.5"


def get_weather_data(url):  # stores data in a dictionary given a url
    # start a session
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)

    # creates soup object
    soup = bs(html.text, "html.parser")

    # stores results in dictionary
    result = {'region': soup.find("div", attrs={"id": "wob_loc"}).text,
              'temp_now': soup.find("span", attrs={"id": "wob_tm"}).text,
              'dayhour': soup.find("div", attrs={"id": "wob_dts"}).text,
              'weather_now': soup.find("span", attrs={"id": "wob_dc"}).text,
              'precipitation': soup.find("span", attrs={"id": "wob_pp"}).text,
              'humidity': soup.find("span", attrs={"id": "wob_hm"}).text,
              'wind': soup.find("span", attrs={"id": "wob_ws"}).text}

    # get next days weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # gets day name
        day_name = day.findAll("div")[0].attrs['aria-label']
        # gets weather for day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # max temp
        max_temp = temp[0].text
        # min temp
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    # add to result
    result['next_days'] = next_days
    return result


if __name__ == "__main__":
    # google search url
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    # place we're searching
    place = "brisbane"
    URL += place
    # get the data
    data = get_weather_data(URL)

    print("Weather for:", data["region"])
    print("Now:", data["dayhour"])
    print(f"Temperature now: {data['temp_now']}°C")
    print("Description:", data['weather_now'])
    print("Precipitation:", data["precipitation"])
    print("Humidity:", data["humidity"])
    print("Wind:", data["wind"])
    print("Next days:")
    for dayweather in data["next_days"]:
        print("="*40, dayweather["name"], "="*40)
        print("Description:", dayweather["weather"])
        print(f"Max temperature: {dayweather['max_temp']}°C")
        print(f"Min temperature: {dayweather['min_temp']}°C")
