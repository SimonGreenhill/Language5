# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string
import random
from django.db import models, migrations

def add_db_user(apps, schema_editor):
    pw = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
    User = apps.get_model("auth", "User")
    u = User.objects.create(username='mr-database', password=pw)
    u.save()

class Migration(migrations.Migration):
    dependencies = [('core', '0002_fix_classification'),]
    operations = [migrations.RunPython(add_db_user),]
 