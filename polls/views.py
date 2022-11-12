from django.shortcuts import render, redirect
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv
import os 

load_dotenv() 
def index_func(request):
    res = 0
    if request.method == 'POST':
        name = request.POST['Name']
        year = request.POST['year']
        fuel = request.POST['fuel']
        seats = request.POST['seats']
        mil = request.POST['mil']
        owner = request.POST['owner']
        isAdvancedSearch = int(request.POST.get('advancedInput'))

        #km = request.POST['km']
        #dealer = request.POST['dealer']
        #trans = request.POST['trans']
        #rpm = request.POST['rpm']
        #eng = request.POST['eng']
        #power = request.POST['power']
        
        print('#####################')
        Ownership = Helper(owner)

        basic_columns = ['year','fuel','seats','mil_kmpl', 'First Owner','Fourth & Above Owner',
                        'Second Owner','Test Drive Car','Third Owner']
        advanced_columns = [*basic_columns, 'km_driven','seller_type','transmission',
                            'torque_rpm','engine_cc','max_power_new']
        basic_df2 = {'year': int(year),'fuel': float(fuel),
                       'seats': int(seats),'mil_kmpl': float(mil),
                       'First Owner': Ownership[0],'Fourth & Above Owner':Ownership[1],'Second Owner': Ownership[2],'Test Drive Car': Ownership[3],
                       'Third Owner': Ownership[4]}

        columns = basic_columns
        df2 = basic_df2
        
        if isAdvancedSearch:
            km = request.POST['km']
            dealer = request.POST['dealer']
            trans = request.POST['trans']
            rpm = request.POST['rpm']
            eng = request.POST['eng']
            power = request.POST['power']
            advanced_df2 = {**basic_df2, 'km_driven': float(km),
                       'seller_type': int(dealer),'transmission': int(trans),
                        'torque_rpm': float(rpm),'engine_cc': float(eng),
                       'max_power_new': float(power)}
            columns = advanced_columns
            df2 = advanced_df2
        
        if name != "":
            df = pd.DataFrame(columns=columns)
            # Ownership = Helper(owner)

            df = df.append(df2, ignore_index=True)
            
            if isAdvancedSearch:
                loaded_model = pickle.load(open('polls/CarSelling.pickle', 'rb'))
            else :
                loaded_model = pickle.load(open('polls/CarSelling2.pickle', 'rb'))
            res = loaded_model.predict(df)
            url = "https://api.apilayer.com/fixer/convert?to=USD&from=INR&amount="+ str(res.tolist()[0])

            payload={}
            headers= {
            "apikey": os.getenv('API_KEY')
            }

            try:
                response = requests.request("GET", url, headers=headers, data = payload)
                status_code = response.status_code
                print(status_code)
                result = response.json()
                res = result["result"]
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                
        else:
            return redirect('homepage')
    else:
        pass

    return render(request, "index.html", {'response': res})


def Helper(x):
    if x == '1':
        return [1, 0, 0, 0, 0]
    elif x == '2':
        return [0, 0, 1, 0, 0]
    elif x == '3':
        return [0, 0, 0, 0, 1]
    if x == '4':
        return [0, 1, 0, 0, 0]
    if x == '5':
        return [0, 0, 0, 1, 0]

