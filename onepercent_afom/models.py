import requests
import json
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.dispatch import receiver
from apps.fund.models import Donation, DonationStatuses # Old donation model

# The commented code below is a start to adapt this code to the new donation flow once its ready

#from bluebottle.utils.model_dispatcher import get_donation_model

# DONATION_MODEL = get_donation_model()

# @receiver(pre_save, sender=DONATION_MODEL)
# def post_to_friend_of_mine(sender, created, **kwargs):


@receiver(pre_save, weak=False, sender=Donation)
def post_to_friend_of_mine(sender, instance, **kwargs):

    donation = instance

    # Only post to AFOM for one-off donations. 
    if donation.donation_type != Donation.DonationTypes.one_off:
        return

    # If the instance has no PK the previous status is unknown.
    if donation.pk:
        # NOTE: We cannot check the previous and future state of the ready attribute since it is set in the
        # Donation.save function.

        existing_donation = Donation.objects.get(pk=donation.pk)
        # If the existing donation is already pending, don't mail.
        if existing_donation.status in [DonationStatuses.pending, DonationStatuses.paid]:
            return

    # If the donation status will be pending, send a mail.
    if donation.status in [DonationStatuses.pending, DonationStatuses.paid]:

        if donation.fundraiser:
            identifier = donation.fundraiser.owner.username
        else:
            identifier = donation.project.owner.username

        payload = {}
        payload['identifier'] = identifier # A Friend of Mine has a list of predefined accounts
        payload['amount'] = donation.amount

        if donation.project:
            payload['project'] = donation.project.title

        if donation.user:
            payload['first_name'] = donation.user.first_name
            payload['last_name'] = donation.user.last_name
            payload['city'] = donation.user.location
            payload['email'] = donation.user.email

        url = "http://stage-onepercentclub.campaignapps.nl/api/donations/new"
                
        res = requests.post(url, data=json.dumps(payload))
