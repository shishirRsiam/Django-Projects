from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Categories

def add_categories(request):
    context = {}

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        if not Categories.objects.filter(name = category_name).exists():
            category = Categories.objects.create(name = category_name, description = category_description)
            category.save()
        context['error_msg'] = 'Category already exists.'

    return redirect('addpost')
    # return render(request, 'add_categories.html', context)


def view_category():
    Categoriess = Categories.objects.all()

    for category in Categoriess:
        print(category.name)
        print(category.description)

    return redirect('home')