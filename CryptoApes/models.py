from django.db import models
from django.utils import timezone

class stakedToken(models.Model):
    nft = models.CharField(max_length=42)
    last_withdraw = models.DateTimeField("date logged")
    address = models.CharField(max_length=42)

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.last_withdraw)
        return f"'{self.nft}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

class userBalance(models.Model):
    address = models.CharField(max_length=42)
    balance = models.BigIntegerField()

    def __str__(self):
        """Returns a string representation of a message."""
        return f"'{self.address}' has {self.balance}"