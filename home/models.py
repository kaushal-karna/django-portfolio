from django.db import models


class ContactMessage(models.Model):
    """Stores every message submitted via the contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
