from django.db import models

# Create your models here.

class Visit(models.Model):
    
    visit_id = models.CharField(
        max_length = 255,
        primary_key = True,
    )
    
    kam_id = models.CharField(
        max_length = 255,
    )


    company_name = models.CharField(
        max_length = 255,
    )

    date_of_visit = models.DateTimeField(
        null=True,
        blank=True
    )

    visit_type = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    visit_start_remark = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    visit_close_remark = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    visit_image_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    first_initiated = models.DateTimeField(
        null=True,
        blank=True
    )

    last_updated = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        null=True,
        blank=True,
        max_length=255,
    )

    visited = models.BooleanField()
    manager = models.BooleanField()


class Purpose(models.Model):
    purpose = models.CharField(
        max_length=255,
        primary_key=True,
    )


#### Current Purposes
'''
    Sales Presentation
    Sales Deeal Closing
    Sales callablePricing Discussion
    Order Collection
    Lead Generation
    Key Decision Maker Visit
    Dispute Resolution
'''