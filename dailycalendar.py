from PIL import Image, ImageFont, ImageDraw, ImageOps
from inky.auto import auto
import datetime, requests, random, textwrap
from pathlib import Path

# Display Settings
display = auto()
resolution = display.resolution
output = Image.new("RGB",resolution, (255,255,255))
content = ImageDraw.Draw(output)

# Initialize
todaysDate = datetime.datetime.now()


# app = Flask(__name__)
# @app.route('/img')
# def main():
#     return render_template("index.html")

# @app.route('/success', methods = ['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(f.filename)
#         return render_template("Acknowledgement.html", name = f.filename)
    
# if __name__ == '__main__':
#     app.run(debug=True)

# Weather
class Weather:
    headerClr = ()
    multiLineEvent = ""
    warningIco = ""
    precipLIco = ""
    precipRIco = ""
    def __init__(self, weatherURL, alertsURL):
        self.weatherURL = weatherURL
        self.alertsURL = alertsURL

    def getData(self):
        try:
            forecastResponse = requests.get(self.weatherURL)
            forecastResponse.raise_for_status()
            alertsResponse = requests.get(self.alertsURL)
            alertsResponse.raise_for_status()

            jsonForecast = forecastResponse.json()
            # Left weather
            periodL = jsonForecast['properties']['periods'][0]
            self.timeOfDayL = periodL['name']
            self.dayTemp = periodL['temperature']
            self.precipL = periodL['shortForecast']
            precipChanceValL = periodL['probabilityOfPrecipitation']['value']

            # Right weather
            periodR = jsonForecast['properties']['periods'][1]
            self.timeOfDayR = periodR['name']
            self.nightTemp = periodR['temperature']
            self.precipR = periodR['shortForecast']
            precipChanceValR = periodR['probabilityOfPrecipitation']['value']

            if precipChanceValL != None:
                self.precipChanceValL = precipChanceValL
            else:
                self.precipChanceValL = 0

            if precipChanceValR != None:
                self.precipChanceValR = precipChanceValR
            else:
                self.precipChanceValR = 0

            if alertsResponse.status_code == 200:
                jsonAlert = alertsResponse.json()
                if 'features' in jsonAlert and jsonAlert['features']:
                    event = jsonAlert['features'][0]['properties']['event']
                    eventSplit = event
                    self.multiLineEvent = textwrap.fill(text=eventSplit,width=12)
                    # self.multiLineEvent = '\n'.join(eventSplit)
                    self.warningIco = "\ue002"
                    self.headerClr = (255,0,1)
                    print("Weather alert found.")
                else:
                    print("No weather alerts found.")
                    self.warningIco = ' '
                    self.headerClr = (0,0,0)
        except:
            print("An error occurred while retrieving weather information.")
            self.timeOfDayL = " "
            self.dayTemp = 0
            self.precipChanceValL = 0

            self.timeOfDayR = " "
            self.nightTemp = 0
            self.precipChanceValR = 0
    
        return self.timeOfDayL, self.dayTemp, self.precipChanceValL, self.timeOfDayR, self.nightTemp, self.precipChanceValR, self.warningIco, self.headerClr, self.multiLineEvent
    def iconInit(self):
        day_icons = {
            "Partly": "\uf172",
            "Mostly": "\uf172",
            "Cloudy": "\ue2bd",
            "Rain": "\uf176",
            "Showers": "\uf176",
            "Thunderstorms": "\uebdb",
            "Windy": "\uefd8",
            "Fog": "\ue818"
        }
        
        night_icons = {
            "Partly": "\uf174",
            "Mostly": "\uf174",
            "Cloudy": "\ue2bd",
            "Rain": "\uf176",
            "Showers": "\uf176",
            "Thunderstorms": "\uebdb",
            "Windy": "\uefd8",
            "Fog": "\ue818"
        }
        def getIcon(time_of_day, condition):
            if time_of_day in ["Today","This Afternoon"]:
                for key in day_icons:
                    if key in condition:
                        print(f"Match found: {key} in {condition}, returning {day_icons[key]}")
                        return day_icons[key]
                return "\ue81a"
            elif time_of_day in ["Tonight","Overnight"]:
                for key in night_icons:
                    if key in condition:
                        print(f"Match found: {key} in {condition}, returning {night_icons[key]}")
                        return night_icons[key]
                return "\uef44"
            else:
                for key in day_icons:
                    if key in condition:
                        print(f"Match found: {key} in {condition}, returning {day_icons[key]}")
                        return day_icons[key]
                return "\ue81a"
        self.precipLIco = getIcon(self.timeOfDayL, self.precipL)
        self.precipRIco = getIcon(self.timeOfDayR, self.precipR)

        print(f"Left Icon: {self.precipLIco}")
        print(f"Right Icon: {self.precipRIco}")
        return self.precipLIco, self.precipRIco
## Initialize Weather
weatherLoad = Weather("https://api.weather.gov/gridpoints/LWX/97,71/forecast","https://api.weather.gov/alerts/active?area=DC")
weatherLoad.getData()
weatherLoad.iconInit()

mainLabel = ImageFont.truetype("/home/excelsior/Documents/Projects/Calendar/inky/fonts/Manrope-VariableFont_wght.ttf",30)
mainLabel.set_variation_by_axes([800])

mainContextual = ImageFont.truetype("/home/excelsior/Documents/Projects/Calendar/inky/fonts/Manrope-VariableFont_wght.ttf",15)
mainContextual.set_variation_by_axes([500])
antonRegular = ImageFont.truetype("/home/excelsior/Documents/Projects/Calendar/inky/fonts/Anton-Regular.ttf",200)

materialRegular = ImageFont.truetype("/home/excelsior/Documents/Projects/Calendar/inky/fonts/MaterialSymbolsSharp[FILL,GRAD,opsz,wght].ttf",30)

materialRegular.set_variation_by_axes([1,200])

headerHeight = int(display.height * (2 / 10.0))
bottomMargin = headerHeight + int(display.height * (7.75 / 10.0))
dateNumPos = int(display.height / 2)

screenSize = headerHeight + int(display.height)

imgScreen = int(display.width / 3)
imgScreen2 = int(display.width - imgScreen)
imgSize = (imgScreen2, display.height)

class imageLoad:
    def __init__(self,path,credits=None):
        self.path = path
        self.credits = credits
        self.imgDict = {}
    def images(self):
        imgs = Path(self.path)
        imgList = list(imgs.glob("*"))
        random_img = random.choice(imgList)
        try:
            for img in imgList:
                imgOut = Image.open(random_img)
                imgOuttest = ImageOps.fit(imgOut, imgSize)
                output.paste(imgOuttest,(imgScreen,headerHeight))
            print("Loading " + str(random_img) + "...")
            content.text((0, bottomMargin), f"Last updated: {str(todaysDate.strftime('%m-%d %H:%M'))}", font=mainContextual, fill=(0,0,0), anchor="ls")
        except:
            print("There was an issue loading the images.")

imageloading = imageLoad('/home/excelsior/Documents/Projects/Calendar/inky/img')
imageloading.images()

for y in range(0,headerHeight):
    for x in range(0, display.width):
        output.putpixel((x,y), weatherLoad.headerClr)

fontColor = (255,255,255)
dateFontColor = (0,0,0)

# text
content.text((20,headerHeight/2), "Washington, D.C.", font=mainLabel, fill=fontColor, anchor="lm")

content.text((340, (headerHeight/3)-2), weatherLoad.warningIco, font=materialRegular, fill=fontColor, anchor="mm")
content.multiline_text((340, (headerHeight/3)*2), weatherLoad.multiLineEvent, font=mainContextual, fill=fontColor, anchor="mm", align='center', spacing=1)

content.multiline_text((445, (headerHeight/2)), f"{str(weatherLoad.timeOfDayL)}\n{str(weatherLoad.precipChanceValL)}%", font=mainContextual, fill=fontColor, anchor="mm", spacing=32, align="center")
content.text((410, (headerHeight/2)), weatherLoad.precipLIco, font=materialRegular, fill=fontColor, anchor="rm")
content.text((445, (headerHeight/2)), f"{str(weatherLoad.dayTemp)}°F", font=mainLabel, fill=fontColor, anchor="mm")

content.multiline_text((550, (headerHeight/2)), f"{str(weatherLoad.timeOfDayR)}\n{str(weatherLoad.precipChanceValR)}%", font=mainContextual, fill=fontColor, anchor="mm", spacing=32, align="center")
content.text((515, (headerHeight/2)), weatherLoad.precipRIco, font=materialRegular, fill=fontColor, anchor="rm")
content.text((550, (headerHeight/2)), f"{str(weatherLoad.nightTemp)}°F", font=mainLabel, fill=fontColor, anchor="mm")

content.multiline_text((20, screenSize/2), todaysDate.strftime("%B\n%A"), font=mainLabel, fill=dateFontColor, anchor="lm", spacing=195)
content.text((20, screenSize/2), todaysDate.strftime("%d"), font=antonRegular, fill=dateFontColor, anchor="lm")

def displayOutput():
    display.set_image(output)
    display.show()

displayOutput()