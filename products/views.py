from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category


def product_list(request):
    products = Product.objects.all()
    print(products)
    return render(request, "products/products_list.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/products_detail.html", {"product": product})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "products/category_list.html", {"categories": categories})


def category_detail(request, id):
    # Correction : On utilise 'pk' (l'argument reçu) pour chercher la catégorie
    category = get_object_or_404(Category, id=id)
    products = (
        category.products.all()
    )  # Utilisation du related_name défini dans le modèle
    return render(
        request,
        "products/category_detail.html",
        {"category": category, "products": products},
    )


def add_to_cart(request, product_id):
    # 1. Récupérer le panier actuel en session ou en créer un vide
    cart = request.session.get("cart", {})

    # 2. Ajouter le produit (ou augmenter la quantité)
    product_id_str = str(product_id)  # Les clés de session doivent être des chaînes
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    # 3. Sauvegarder le panier dans la session
    request.session["cart"] = cart

    # 4. Rediriger vers la page précédente ou le panier
    return redirect("product_list")  # Ou vers la page 'cart_detail' plus tard


def cart_detail(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_cart_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity
        total_cart_price += total_price
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "total_price": total_price,
            }
        )

    return render(
        request,
        "products/cart_detail.html",
        {"cart_items": cart_items, "total_cart_price": total_cart_price},
    )


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session["cart"] = cart
    return redirect("cart_detail")
