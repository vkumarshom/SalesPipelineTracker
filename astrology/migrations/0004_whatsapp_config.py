from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('astrology', '0003_fix_profile_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsAppConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text="WhatsApp phone number with country code (e.g., +447123456789)", max_length=128, region=None)),
                ('default_message', models.CharField(default="Hello, I'd like to book an astrology consultation.", help_text="Default message that will be pre-filled when users click to contact via WhatsApp", max_length=255)),
                ('display_name', models.CharField(default="MetaMystic Astrology", help_text="Name to display in the chat widget", max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'WhatsApp Configuration',
                'verbose_name_plural': 'WhatsApp Configurations',
            },
        ),
    ]