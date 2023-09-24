import random

from datetime import datetime
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView

from .models import Recipe, Plan, RecipePlan, DayName


class IndexView(View):

    def get(self, request):
        recipes = list(Recipe.objects.all())
        random.shuffle(recipes)
        ctx = {"actual_date": datetime.now(),
               'first_recipe': recipes[:1],
               'second_recipe': recipes[1:2],
               'third_recipe': recipes[2:3]}
        return render(request, "index.html", ctx)


def dashboard(request):
    if request.method == "GET":
        recipes_quantity = Recipe.objects.count()
        plan_quantity = Plan.objects.count()
        all_plans_list = Plan.objects.all().order_by('-created')
        last_plan = all_plans_list[:1]
        last_plan_details = RecipePlan.objects.all().filter(plan=last_plan)
        context = {'recipes_quantity': recipes_quantity,
                   'plan_quantity': plan_quantity,
                   'last_plan': last_plan,
                   'last_plan_details': last_plan_details}
        return render(request, "dashboard.html", context=context)


def recipes_list(request):

    all_recipes_list = Recipe.objects.all().order_by('-votes', 'created').values()
    paginator = Paginator(all_recipes_list, 50)

    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    context = {'recipes': recipes}

    return render(request, 'app-recipes.html', context)


def plan_list(request):

    all_plans_list = Plan.objects.all().order_by('name')
    paginator = Paginator(all_plans_list, 50)

    page = request.GET.get('page')
    plans = paginator.get_page(page)

    context = {'plans': plans}

    return render(request, 'app-schedules.html', context)


class RecipeAdd(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparing = request.POST.get('preparing')

        if not name:
            message = "Należy podać nazwę przepisu"
        elif not description:
            message = "Należy podać opis przepisu"
        elif not preparation_time:
            message = "Należy podać czas przygotowania"
        elif not preparing:
            message = "Należy podać sposób przygotowania"
        elif not ingredients:
            message = "Należy podać składniki"
        else:
            recipes = Recipe.objects.create(
                name=name,
                ingredients=ingredients,
                description=description,
                preparation_time=preparation_time,
                preparing=preparing)
            return redirect(f'/recipe/list/')
        return render(request, 'app-add-recipe.html', {'message': message})
# class RecipeModify(View):
#     def get(self, request, recipe_id):
#         recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
#         context = {
#             'recipe': recipe
#         }
#         return render(request, 'app-edit-recipe.html', context)
#
#     def post(self, request, recipe_id):
#         try:
#             recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
#         except FieldError:
#             raise Http404
#
#         recipe.name = request.POST.get('name')
#         recipe.description = request.POST.get('description')
#         recipe.preparation_time = request.POST.get('preparation_time')
#         recipe.ingredients = request.POST.get('ingredients')
#
#         if not recipe.name or not recipe.description or not recipe.preparation_time or not recipe.ingredients:
#             messages.error(request, 'Wypełnij poprawnie wszystkie pola')
#             return redirect('recipe/modify/<int:recipe_id>/')
#
#         recipe.save()
#         return redirect('recipe/<int:recipe_id>/')

class RecipeEdit(View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return render(request, 'app-edit-recipe.html', {'recipe': recipe})

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        new_name = request.POST.get('new_name')
        new_ingredients = request.POST.get('new_ingredients')
        new_description = request.POST.get('new_description')
        new_preparation_time = request.POST.get('new_preparation_time')
        new_preparing = request.POST.get('new_preparing')

        if new_name is not None and new_name != '':
            recipe.name = new_name
            recipe.save()
        if new_ingredients is not None and new_ingredients !='':
            recipe.ingredients = new_ingredients
            recipe.save()
        if new_description is not None and new_description != '':
            recipe.description = new_description
        if new_preparation_time is not None and new_preparation_time !='':
            recipe.preparation_time = new_preparation_time
        if new_preparing is not None and new_preparing != '':
            recipe.preparing = new_preparing
        # if recipe.name != new_name:
        #     recipe.name = new_name
        # if recipe.ingredients != new_ingredients:
        #     recipe.ingredients = new_ingredients
        # if recipe.description != new_description:
        #     recipe.description = new_description
        # if recipe.preparation_time != new_preparation_time:
        #     recipe.preparation_time = new_preparation_time
        # if recipe.preparing != new_preparing:
        #     recipe.preparing = new_preparing
        recipe.votes = 0
        recipe.save()
        return redirect(f'/recipe/list/')
        # message = f"Nowy przepis na podstawie przepisu bazowego został stworzony"
        # return render(request, 'app-recipes.html', {'message': message})


class PlanAdd(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            message = "Należy podać nazwę planu"
            return render(request, 'app-add-schedules.html', {'message': message})
        elif not description:
            message = "Należy podać opis planu"
            return render(request, 'app-add-schedules.html', {'message': message})
        else:
            message = "Plan został pomyślnie dodany"
            plan = Plan.objects.create(name=name, description=description)
            plans = Plan.objects.all().order_by('-created')
            context = {'message': message,
                       'plans': plans}
            return render(request, 'app-schedules.html', context=context)


def plan_details(request, id):
    plan_detail = Plan.objects.get(id=id)
    try:
        recipes_plan = RecipePlan.objects.all().filter(plan_id=id)
        context = {'plan_detail': plan_detail,
                   'recipes_plan': recipes_plan}
    except RecipePlan.DoesNotExist:
        context = {'plan_detail': plan_detail}
    return render(request, 'app-details-schedules.html', context=context)


def recipe_details(request, id):
    recipe = Recipe.objects.get(id=id)

    if request.method == "POST":
        if 'like' in request.POST:
            recipe.votes += 1
        elif 'dislike' in request.POST:
            recipe.votes -= 1

        recipe.save()
        message = "Twój głos został dodany. Dziękujemy za udział w głosowaniu"
        return render(request, 'app-recipe-details.html', {'recipe': recipe, 'message': message})

    return render(request, 'app-recipe-details.html', {'recipe': recipe})


class PlanAddRecipeView(View):
    def get(self, request):
        plans = Plan.objects.all().order_by('name')
        recipes = Recipe.objects.all().order_by('name')
        days = DayName.objects.all().order_by('order')
        context = {'plans': plans,
                   'recipes': recipes,
                   'days': days}
        return render(request, 'app-schedules-meal-recipe.html', context=context)

    def post(self, request):
        selected_plan = request.POST.get('selected_plan')
        meal_name = request.POST.get('meal_name')
        meal_number = request.POST.get('meal_number')
        selected_recipe = request.POST.get('selected_recipe')
        day_name = request.POST.get('day_name')

        plan = Plan.objects.get(pk=selected_plan)
        recipe = Recipe.objects.get(pk=selected_recipe)
        day = DayName.objects.get(pk=day_name)

        # recipe_plan = RecipePlan()
        # recipe_plan.plan_id = plan.id
        # recipe_plan.meal_name = meal_name
        # recipe_plan.order = meal_number
        # recipe_plan.recipe_id = recipe.id
        # recipe_plan.day_name_id = day.id
        # recipe_plan.save()
        #
        # return redirect(f'/plan/{plan.id}/')

        # if not selected_plan:
        #     message = "Należy wybrać nazwę planu"
        # elif not meal_name:
        #     message = "Należy podać nazwę posiłku"
        # elif not meal_number:
        #     message = "Należy podać numer posiłku"
        # elif not selected_recipe:
        #     message = "Należy podać wybrać posiłek"
        # elif not day_name:
        #     message = "Należy wybrać dzień"
        # if recipe.preparing is None and recipe.preparing == '':
        #     recipe.preparing = "nie podano sposobu przygotowania"
        #
        #     recipe_plan = RecipePlan.objects.create(
        #         meal_name=meal_name,
        #         recipe=recipe,
        #         plan=plan,
        #         order=meal_number,
        #         day_name=day)

            # message = "Przepis został dodany do planu"
        # return redirect(f'/plan/{plan.id}/')
        # return render(request, 'app-schedules-meal-recipe.html')

