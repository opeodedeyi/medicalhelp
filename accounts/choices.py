from .models import Sickness


duration_choices = {
    '0-1 week':'0-1 week',
    '2 weeks':'2 weeks',
    '3 weeks':'3 weeks',
    '4 weeks':'4 weeks',
    '5+ weeks':'5+ weeks',
}

sickness_choices = {
    i.id: i.name for i in Sickness.objects.all()
}
        