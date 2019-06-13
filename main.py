import http.client as h
import json
import telebot


cities = {
    "Moscow": ["55.75396", "37.620393"],
    "SaintPetersburg": ["59.939095", "30.315868"],
    "Sochi": ["43.585525", "39.723062"],
    "Peterhof": ["59.883330", "29.900"],
    "London": ["51.5073509", "-0.1277583"],
    "Berlin": ["52.5200066", "13.404954"],
    "Karaganda": ["49.8333300", "73.1658000"]
}


def get_forecast(lat, lon):
    conn = h.HTTPSConnection("api.weather.yandex.ru")
    conn.request("GET", "/v1/forecast?lat=" + lat + "&lon=" + lon + "&limit=1",
                 headers={
                     "X-Yandex-API-Key": "4a85cba5-d2a6-433e-871f-6c0f67d6fcde"
                 })
    response = conn.getresponse()
    res = json.load(response)
    return res


# def parse_answer(weather_answer):
#     tom_d = get_tomorrow_date(weather_answer["now_dt"].split('T')[0
#     cws = 0
#     res_str = ""
#     for i in weather_answer["forecasts"]:
#         if tom_d == i["date"]:
#             cws = i["parts"]["day_short"]
#     if cws != 0:
#         res_str += "Temperature:" + str(cws["temp"])
#         res_str += "\nWind speed: " + str(cws["wind_speed"])
#         res_str += "\nWind direction " + str(cws["wind_dir"])
#         res_str += "\n" + str(cws["condition"])
#
#     return res_str


def parse_answer(weather_answer):
    tom_d = get_tomorrow_date(weather_answer["now"])
    cws = 0
    res_str = ""
    for i in weather_answer["forecasts"]:
        if int(tom_d) > int(i["date_ts"]):
            cws = i["parts"]["day_short"]
    if cws != 0:
        res_str += "Temperature: " + str(cws["temp"])
        res_str += "\nWind speed: " + str(cws["wind_speed"])
        res_str += "\nWind direction " + str(cws["wind_dir"])
        res_str += "\n" + str(cws["condition"])
    return res_str


def parse_answer_today(weather_answer):
    tom_d = weather_answer["now"]
    cws = 0
    res_str = ""
    cws = weather_answer["fact"]
    if cws != 0:
        res_str += "Temperature: " + str(cws["temp"])
        res_str += "\nWind speed: " + str(cws["wind_speed"])
        res_str += "\nWind direction " + str(cws["wind_dir"])
        res_str += "\n" + str(cws["condition"])
    return res_str


def get_tomorrow_date(date):
    return str(int(date) + 86400)


bot = telebot.TeleBot("894480080:AAH5CGQulI-y00ldJxJN7YPDsizRmszw_Jg")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello there ladies and gentleman! "
                          "Allow me to introduce myself. "
                          "My name is weatherBot and i provide weather info. "
                          "Type '/get_weather *town_name*' for current information on the area. "
                          "Type '/get_forecast *town_name*' to find out tomorrow average temperature and weather.")


@bot.message_handler(commands=['get_forecast'])
def send_tomorrow_weather(message):
    text = message.text.split()[1]
    if text not in cities.keys():
        bot.reply_to(message, "invalid city")
        return
    coords = cities[text]
    result = get_forecast(coords[0], coords[1])
    result_str = parse_answer(result)
    bot.reply_to(message, result_str)


@bot.message_handler(commands=['get_weather'])
def send_today_weather(message):
    text = message.text.split()[1]
    if text not in cities.keys():
        bot.reply_to(message, "invalid city")
        return
    coords = cities[text]
    result = get_forecast(coords[0], coords[1])
    result_str = parse_answer_today(result)
    bot.reply_to(message, result_str)



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Sorry? Try to type '/get_forecast *Town_name*'.")


# res = get_forecast("55.75396", "37.620393")
bot.polling()
# print(get_tomorrow_date("2016-08-03"))
