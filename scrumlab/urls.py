"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from jedzonko.views import IndexView, RecipeAdd, PlanAdd, PlanAddRecipeView, RecipeEdit
from jedzonko.views import dashboard, recipes_list, plan_details, recipe_details, plan_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', IndexView.as_view()),
    path('main/', dashboard),
    path('recipe/add/', RecipeAdd.as_view()),
    path('recipe/edit/<int:recipe_id>', RecipeEdit.as_view()),
    path('plan/add/', PlanAdd.as_view()),
    path('plan/list/', plan_list),
    path('recipe/list/', recipes_list),
    path('plan/add-recipe/', PlanAddRecipeView.as_view()),
    path('recipe/<int:id>/', recipe_details),
    path('plan/<int:id>/', plan_details),


]



