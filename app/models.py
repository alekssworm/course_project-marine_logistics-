"""
Definition of models.
"""
from django.core.validators import MaxValueValidator , MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'custom_user'

class Port(models.Model):
    port_table_id = models.AutoField(primary_key=True)
    port_name = models.TextField()
    port_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    port_longitude = models.DecimalField(max_digits=9, decimal_places=6)



    def __str__(self):
        return self.port_name

    class Meta:
        db_table = 'port_table'


from django.db import models
from decimal import Decimal

class Ship(models.Model):
    ship_table_id = models.AutoField(primary_key=True)
    name_of_vessel = models.TextField()
    ship_tonnage = models.PositiveIntegerField()
    ship_type = models.CharField(max_length=100)
    home_port = models.ForeignKey(Port, on_delete=models.SET_NULL, null=True, blank=True)
    average_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    crew = models.PositiveIntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.name_of_vessel

    class Meta:
        db_table = 'ship_table'
        
from django.db import models
from .models import Ship

class CrewPayment(models.Model):
    payment_date = models.DateField()
    amount_crew = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ship_table = models.ForeignKey(Ship, on_delete=models.CASCADE)

    def __str__(self):
        return f"Crew Payment for {self.ship_table.name_of_vessel} on {self.payment_date}"

    class Meta:
        db_table = 'crew_payment'



class ShipRepair(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    repair_start_date = models.DateField()
    repair_end_date = models.DateField()
    cost_repair = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Repair of {self.ship.name_of_vessel} from {self.repair_start_date} to {self.repair_end_date}"

    class Meta:
        db_table = 'ship_repair'


from django.db.models import Sum
from django.core.exceptions import ValidationError
from decimal import Decimal

class WritingAContract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    cargo_quantity = models.IntegerField()
    type_of_cargo = models.TextField(blank=True)
    port_id_with_cargo = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='contracts_with_cargo')
    port_final_destination = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='contracts_final_destination')
    customer_addendum = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contracts')
    temperature_mode = models.TextField(blank=True)
    in_work = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contracts_created')

    
    def clean(self):
        if self.port_id_with_cargo == self.port_final_destination:
            raise ValidationError("The cargo port and the final destination port cannot be the same!")

        if self.cargo_quantity < 0:
            raise ValidationError("The amount of cargo cannot be negative!")

        
        if 'temperature_mode' in self.cleaned_data and 'temperature_value' in self.cleaned_data and 'temperature_unit' in self.cleaned_data:
            temperature_mode = self.cleaned_data['temperature_mode']
            temperature_value = self.cleaned_data['temperature_value']
            temperature_unit = self.cleaned_data['temperature_unit']

            
            if temperature_value is not None:
                temperature_mode += f' {temperature_value} {temperature_unit}'

            self.cleaned_data['temperature_mode'] = temperature_mode

    def __str__(self):
        return str(self.contract_id)

    class Meta:
        db_table = 'writing_a_contract'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateField(null=True, default=None)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_made = models.BooleanField(default=False)
    contract = models.ForeignKey(WritingAContract, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"Payment ID: {self.payment_id}"

    class Meta:
        db_table = 'payment'


class Assignment(models.Model):
    contract = models.ForeignKey('WritingAContract', on_delete=models.CASCADE)
    ship_table = models.ForeignKey('Ship', on_delete=models.CASCADE)
    vessel_load_calculation = models.PositiveIntegerField(default=0)




from django.db.models import Max
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class RouteShip(models.Model):
    ship_table = models.ForeignKey(Ship, on_delete=models.CASCADE)
    from_the_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='route_departures')
    to_the_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='route_arrivals')
    voyage_duration = models.PositiveIntegerField()
    time_to_port = models.DateTimeField()
    order_completed = models.BooleanField(default=False)
    route_key = models.CharField(max_length=255, unique=True, null=True, blank=True)

    class Meta:
        db_table = 'route_ship'




class ShippingCost(models.Model):
    cargo_type = models.CharField(max_length=100, unique=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cargo_type
    class Meta:
        db_table = 'ShippingCost'