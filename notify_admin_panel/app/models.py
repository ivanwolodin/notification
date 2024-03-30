from django.db import models
from ckeditor.fields import RichTextField


class Channels(models.TextChoices):

    email = "email", "email"
    sms = "notifications", "notifications"


class Template(models.Model):
    name = models.CharField("name", max_length=255)
    subject = models.CharField("subject", max_length=255)
    content = RichTextField(
        "content",
        help_text="в шаблоне можно использовать переменные {{name}} - имя и {{content}} - содержание уведомления",
    )
    channel = models.TextField("channel", choices=Channels.choices,
                               max_length=13)

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    def __str__(self) -> str:
        return f"{self.name} {self.channel}"


class Notification(models.Model):
    channel = models.TextField("channel", choices=Channels.choices,
                               max_length=13)
    name = models.CharField("name", max_length=255)
    content = RichTextField(
        "content",
    )
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE,
        verbose_name="template"
    )
    plan_date = models.DateTimeField()
    processed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
