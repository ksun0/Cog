from django.contrib.auth.models import User; from Dashboard.models import *; user=User.objects.all()[0];prof=user.profile; users=list(User.objects.all()); tasks=prof.task_set.get_queryset(); events=prof.event_set.get_queryset(); tt=TaskType.objects.all()[0];
