from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def catalog(request):
    products = Product.objects.filter(activo=True).select_related('category', 'stl_model')
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    tipo = request.GET.get('tipo')
    if tipo:
        products = products.filter(category__tipo=tipo)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'selected_tipo': tipo,
        'query': query,
    }
    return render(request, 'store/catalog.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, activo=True)
    stl_url = None

    if product.tiene_stl:
        stl_url = product.stl_model.file.url

    context = {
        'product': product,
        'stl_url': stl_url,
    }
    return render(request, 'store/product_detail.html', context)


def filaments(request):
    filamentos = Product.objects.filter(activo=True, category__tipo='filamento').select_related('category')
    consumibles = Product.objects.filter(activo=True, category__tipo='consumible').select_related('category')

    return render(request, 'store/filaments.html', {
        'filamentos': filamentos,
        'consumibles': consumibles,
    })
