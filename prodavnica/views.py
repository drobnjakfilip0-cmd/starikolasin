from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import messages
# Create your views here.
def market(request):
    products = Product.objects.all()
    return render(request, 'prodavnica/market.html', {
        'products': products
    })


def contact_product(request):
    if request.method == "POST":

        product = get_object_or_404(Product, id=request.POST['product_id'])
        user_email = request.POST['email']

        html_message = render_to_string(
                "prodavnica/email.html",
                {
                    'ime': product.ime,
                    'opis': product.opis,
                }
            )
        # 1. Auto-reply korisniku
        send_mail(
            subject="Успешно сте нас контактирали",
            message="",
            from_email="drobnjakfilip0@gmail.com",
            recipient_list=[user_email],
            html_message=html_message
        )
        messages.success(request, "Успешно сте нас контактирали. Ускоро Вам се јављамо путем мејла.")


    return redirect('prodavnica:market')