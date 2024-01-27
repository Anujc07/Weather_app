from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import urllib.request
import json

def Index(request):
    if request.method=='POST':
        Email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=Email, password=password)
        if user is not None:
            login(request, user)
            return render(request,'main.html')
        else :
            messages.error(request, 'Wrong email or password')
    return render(request,'index.html')

# def Main(request):
     
#     return render(request,'main.html')

def Signup(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        Pass=request.POST.get('password')
        user = User.objects.create_user(username=uname,email=email,password=Pass)
        login(request, user)
        return render(request,'main.html')
    return render(request,'signup.html')

@login_required(login_url='login')
def Main(request):
    if request.method == "POST":
        key = "7e15f0fecea1ff48202ecd8fad751f69"
        city = request.POST.get("city")
        if city:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
                source = urllib.request.urlopen(url).read()
                data = json.loads(source)
                print("*******This is data**********")
                print(data)
                weather_data = data.get("main")
                print("*******This is weather data**********")
                print(weather_data)
                kelvin_temp = data['main']['temp']
                celsius_temp = round(kelvin_temp - 273.15, 2)  
                wind_speed_mps = data.get('wind', {}).get('speed', 0)  
                wind_speed_kmph = round(wind_speed_mps * 3.6, 2)    
                feels_like_kelvin = data.get('main', {}).get('feels_like', 0) 
                feels_like_celsius = round(feels_like_kelvin - 273.15, 2)  
                feels_like_fahrenheit = round((feels_like_kelvin - 273.15) * 9/5 + 32, 2)  
                return render(request, 'main.html', {'feels_like_celsius': feels_like_celsius,'feels_like_fahrenheit': feels_like_fahrenheit,'data': data, 'city': city,'celsius_temp': celsius_temp,'wind_speed_kmph': wind_speed_kmph})
            except urllib.error.HTTPError as e:
                error_message = f"HTTP Error {e.code}: {e.reason}"
                print(error_message)
                return render(request, 'main.html', {'error_message': error_message})
            except urllib.error.URLError as e:
                error_message = f"URL Error: {str(e.reason)}"
                print(error_message)
                return render(request, 'main.html', {'error_message': error_message})
            except json.JSONDecodeError as e:
                error_message = f"JSON Decode Error: {str(e)}"
                print(error_message)
                return render(request, 'main.html', {'error_message': error_message})
            except Exception as e:
                error_message = f"Error fetching data: {str(e)}"
                print(error_message)
                return render(request, 'main.html', {'error_message': error_message})
        else:
            error_message = "Please enter a city name."
            return render(request, 'main.html', {'error_message': error_message})

    return render(request, 'main.html')