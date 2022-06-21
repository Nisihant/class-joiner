from django.shortcuts import render, HttpResponse
import json
import pandas as pd
from twilio.rest import Client
from class_joiner.settings import ACCOUNT_SID, AUTH_TOKEN

# Create your views here.


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'classJoiner/home.html', context)


def getclasses(request):
    if request.method == 'POST':
        with open("./classJoiner/artifacts/timetable.json") as f:
            _index = json.load(f)

        group = request.POST.get('group')
        day = request.POST.get('day')
        period = request.POST.get('period')
        period = int(float(period))
        dic = dict()
        if period >= 9 or period < 0 or len(_index[group][day][period]) == 1:
            dic = {
                "teacher": "NO CLASS",
                "subject": "NOW YOU ARE FREE",
                "link": "javascript:void(0);"
            }
        else:
            dic = {
                "teacher": _index[group][day][period][0],
                "subject": _index[group][day][period][1],
                "link": _index[group][day][period][2]
            }
        return HttpResponse(json.dumps(dic))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def sendMessage(request):
    if request.method == 'POST':
        # logging to the whatsapp account
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        client = Client(account_sid, auth_token)

        # reading all the receivers
        df = pd.read_csv("./classJoiner/artifacts/phoneNo.csv")

        # loading time table
        with open("./classJoiner/artifacts/timetable.json") as f:
            _index = json.load(f)

        # loading info about class timing
        day = request.POST.get('day')
        period = request.POST.get('period')
        period = int(float(period))

        # sending link of all the classes
        if period >= 9 or period < 0 or period == 4:
            return HttpResponse(json.dumps({"status": "passed"}))

        
        for ind, row in df.iterrows():
            if len(_index[row["group"]][day][period]) > 1:
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="Link: {}\nClass: {}\nTeacher: {}".format(_index[row["group"]][day][period][2], _index[row["group"]][day][period][1], _index[row["group"]][day][period][0]),
                    to='whatsapp:+{}'.format(str(row["phoneNo"]))
                )

        return HttpResponse(json.dumps({"status": "passed"}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


if __name__ == "__main__":
    sendMessage()
