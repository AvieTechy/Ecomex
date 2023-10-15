from django.urls import path

from revenue.views import (
   revenue_view,
   )

app_name = 'revenue'

urlpatterns = [
    #revenue

	path('', revenue_view, name="revenue_view"),


]