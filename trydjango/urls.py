from django.contrib import admin
from django.urls import path, include

from accounts.views import (
  login_view,
  logout_view,
  register_view
)
from .views import home_view


urlpatterns = [
  path('admin/', admin.site.urls),
  path('login/', login_view),
  path('logout/', logout_view),
  path('register/', register_view),
  path('', home_view),  
  path('articles/', include('articles.urls')),  
  path('pantry/recipes/', include('recipes.urls'))
]
