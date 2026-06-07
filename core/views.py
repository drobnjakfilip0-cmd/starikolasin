from django.shortcuts import render, get_object_or_404
from .models import Vest, Video, Rec, Artwork, Film
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.
def index(request):
    vesti = Vest.objects.order_by('-created_at')[:6]
    videos = Video.objects.order_by('-created_at')[:2]
    artworks = Artwork.objects.all()[:5]

    return render(request, 'core/index.html', {
        'vesti': vesti,
        'videos': videos,
        'artworks': artworks,
    })

def vesti(request, pk):
    vest = get_object_or_404(Vest, pk=pk)

    return render(request, 'core/vesti.html', {
        'vest': vest
    })

def about(request):
    return render(request, 'core/about.html')


def rec(request):
    query = request.GET.get("query", "").strip()

    reci = Rec.objects.all()

    if query:
        words = query.split()

        # baza rezultata
        qs = Q()

        for word in words:
            qs |= Q(autor__icontains=word) | Q(naslov__icontains=word)

        reci = reci.filter(qs)

        # 🔥 PostgreSQL fuzzy ranking
        reci = reci.annotate(
            similarity=TrigramSimilarity("naslov", query)
        ).order_by("-similarity")

    reci = reci.order_by("-created")[:5]

    return render(request, "core/rec.html", {
        "reci": reci,
        "query": query
    })
def rec_detail(request, pk):
    rec = get_object_or_404(Rec, pk=pk)
    return render(request, 'core/rec_detail.html', {
        'rec':rec
    })

def bioskop_rezervacija(request):
    import json
    from django.http import JsonResponse
    from django.core.mail import send_mail
    from django.conf import settings

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Dozvoljena samo POST metoda.'}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Neispravni podaci.'}, status=400)

    email     = data.get('email', '').strip()
    ime       = data.get('ime', '').strip()
    film_id   = data.get('film_id')
    film_title = data.get('film_title', '')
    film_date  = data.get('film_date', '')
    film_price = data.get('film_price', '')

    if not email or '@' not in email:
        return JsonResponse({'ok': False, 'error': 'Унесите исправну e-mail адресу.'})

    poruka = (
        f"Нова резервација карте!\n\n"
        f"Филм: {film_title}\n"
        f"Датум и вријеме: {film_date}\n"
        f"Цена: {film_price} РСД\n\n"
        f"Гост: {ime or '(није унето)'}\n"
        f"E-mail: {email}\n"
    )

    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives

    ctx = {
        'film_title': film_title,
        'film_date':  film_date,
        'film_price': film_price,
        'ime':        ime or None,
        'email':      email,
    }
    html_body = render_to_string('core/email_rezervacija.html', ctx)

    try:
        msg = EmailMultiAlternatives(
            subject=f"Резервација — {film_title}",
            body=poruka,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Слање е-поште није успело. Покушајте поново.'})

    return JsonResponse({'ok': True})


def bioskop(request):
    from django.utils import timezone
    featured = Film.objects.filter(featured=True).first()
    films = Film.objects.filter(featured=False).order_by('screening_date')
    return render(request, 'core/bioskop.html', {
        'featured': featured,
        'films': films,
    })


def likovna_kolonija(request):
    artworks = Artwork.objects.all()
    return render(request, 'core/likovna_kolonija.html', {
        'artworks': artworks,
    })

def likovna_kolonija_detail(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug)
    return render(request, 'core/likovna_kolonija_detail.html', {
        'artwork': artwork,
    })
