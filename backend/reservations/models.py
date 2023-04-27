from datetime import datetime
from django.db import models
from users.models import User
from cabins.models import Cabin
from services.models import Service


class Reservation(models.Model):
    """
    User model represents a customer or a staff member.
    """

    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    services = models.ManyToManyField(Service, blank=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)  # When the reservation was created by the customer
    accepted_at = models.DateTimeField(null=True)  # When the reservation was accepted by the owner or staff
    canceled_at = models.DateTimeField(null=True)  # When the reservation was canceled by the customer or staff

    def __str__(self):
        return f"{self.cabin} {self.customer} {self.start_date} {self.end_date}"

    @property
    def length_of_stay(self) -> int:
        start = datetime.strptime(self.start_date.__str__(), "%Y-%m-%d")
        end = datetime.strptime(self.end_date.__str__(), "%Y-%m-%d")
        return (end - start).days

    def get_total_cabin_price(self) -> float:
        """
        Returns the total price of the cabin for the reservation period.
        """
        price = self.cabin.price_per_night * self.length_of_stay
        return price

    def get_total_services_price(self) -> float:
        """
        Returns the total price of the services for the reservation period.
        """
        price = 0
        for service in self.services.all():
            price += service.service_price
        return price

    def get_total_price(self) -> float:
        """
        Returns the total price of the reservation.
        """
        price = self.get_total_cabin_price() + self.get_total_services_price()
        return price

    def get_services(self) -> list:
        """
        Returns all the services that are included in the reservation.
        """
        services = []
        for service in self.services.all():
            services.append((service.name, service.service_price))
        return services


class Invoice(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # When the invoice was created
    paid_at = models.DateTimeField(null=True)  # When the invoice was paid
    canceled_at = models.DateTimeField(null=True)  # When the invoice was canceled

    def __str__(self):
        return f"{self.reservation}"

    @property
    def total_price(self) -> tuple:
        """
        Returns the total price of the reservation.
        """
        total_price = self.reservation.get_total_cabin_price() + self.reservation.get_total_services_price()
        return total_price

    def get_invoice(self) -> str:
        """
        Returns the invoice in PDF format.
        """
        invoice = ""
        return invoice
