from django.contrib import admin
from .models import Travel, QuickDestination, TravelAdvice, WeatherSnapshot

# Enregistre les modèles pour qu'ils apparaissent dans l'admin
# tous viennent du fichier models.py
admin.site.register(Travel)

#admin.site.register(QuickDestination)
#admin.site.register(TravelAdvice)
#admin.site.register(WeatherSnapshot)
