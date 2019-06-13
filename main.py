import http.client as h
import json
import telebot


cities = {
    "Moscow": ["55.75396", "37.620393"],
    "SaintPetersburg": ["59.939095", "30.315868"],
    "Sochi": ["43.585525", "39.723062"],
    "Peterhof": ["59.883330", "29.900"]
}


def get_weather(lat, lon):
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
        res_str += "Temperature:" + str(cws["temp"])
        res_str += "\nWind speed: " + str(cws["wind_speed"])
        res_str += "\nWind direction " + str(cws["wind_dir"])
        res_str += "\n" + str(cws["condition"])

    return res_str


def get_tomorrow_date(date):
    return str(int(date) + 86400)


bot = telebot.TeleBot("894480080:AAH5CGQulI-y00ldJxJN7YPDsizRmszw_Jg")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['get_weather'])
def send_tomorrow_weather(message):
    text = message.text.split()[1]
    if text not in cities.keys():
        bot.reply_to(message, "invalid city")
        return
    coords = cities[text]
    result = get_weather(coords[0], coords[1])
    result_str = parse_answer(result)
    bot.reply_to(message, result_str)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "И че?")


# res = get_weather("55.75396", "37.620393")
bot.polling()
# print(get_tomorrow_date("2016-08-03"))
