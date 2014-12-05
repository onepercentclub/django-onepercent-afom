import requests
import json
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.dispatch import receiver
from bluebottle.utils.model_dispatcher import get_order_model
from bluebottle.utils.utils import StatusDefinition


ORDER_MODEL = get_order_model()


@receiver(pre_save, weak=False, sender=ORDER_MODEL)
def post_to_friend_of_mine(sender, instance, **kwargs): 
    
    for donation in instance.donations.all():
        #donation = instance.donation

        # Don't send to AFOM with anonymous donations
        if donation.anonymous:
            return

        # Only post to AFOM for one-off donations. 
        if donation.order.order_type != 'one-off':
            return

        # If the donation status will be pending, do a request to AFOM.
        if donation.order.status in [StatusDefinition.PENDING, StatusDefinition.SUCCESS]:

            identifier = None
            if donation.fundraiser:
                identifier = donation.fundraiser.owner.username
            else:
                identifier = donation.project.owner.username

            payload = {}
            payload['identifier'] = identifier # Allowed usernames are in the AFOM CMS
            payload['amount'] = int(donation.amount) # Cast decimal to int for JSON

            if donation.project:
                payload['project'] = donation.project.title

            if donation.user:
                payload['first_name'] = donation.order.user.first_name
                payload['last_name'] = donation.order.user.last_name
                payload['city'] = donation.order.user.location
                payload['email'] = donation.order.user.email

            headers = {'content-type': 'application/json'}
            url = "http://stage-onepercentclub.campaignapps.nl/api/donations/new"
            res = requests.post(url, data=json.dumps(payload), headers=headers)

