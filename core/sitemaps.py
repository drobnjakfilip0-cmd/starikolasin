from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Vest, Rec, Artwork


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'core:index',
            'core:about',
            'core:rec',
            'core:bioskop',
            'core:likovna_kolonija',
        ]

    def location(self, item):
        return reverse(item)


class VestSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.7

    def items(self):
        return Vest.objects.order_by('-created_at')

    def location(self, obj):
        return reverse('core:vesti', args=[obj.pk])

    def lastmod(self, obj):
        return obj.created_at


class RecSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.6

    def items(self):
        return Rec.objects.order_by('-created')

    def location(self, obj):
        return reverse('core:rec_detail', args=[obj.pk])

    def lastmod(self, obj):
        return obj.created


class ArtworkSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Artwork.objects.order_by('-created_at')

    def location(self, obj):
        return reverse('core:likovna_kolonija_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.created_at
