import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def donation_trigger(request):
    """
        Test view to trigger the sending of a dummy donation
    """

    if request.method == "GET":
        return Response("Request must be POST")

    if request.method == 'POST':

        payload = {}
        payload['identifier'] = "SjaakTrekhaak"
        payload['first_name'] = "Donny"
        payload['last_name'] = "Donateur"
        payload['city'] = "Amsterdam"
        payload['email'] = "info@onepercentclub.com"
        payload['project'] = "AwesomeAksel"
        payload['amount'] = "280"

        url = "http://stage-onepercentclub.campaignapps.nl/api/donations/new"

        headers = {'content-type': 'application/json'}
        res = requests.post(url, data=json.dumps(payload), headers=headers)

        if res.status_code == 200:
            result = "success"
        else:
            result = "error: {0}".format(res.content)

        return Response(result)

