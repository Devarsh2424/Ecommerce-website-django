from category.models import Category


def menu_links(request):
    links = Category.objects.all()  # Fetch all categories from the database
    return {'links': links}  # Return the categories in a dictionary for use in templates