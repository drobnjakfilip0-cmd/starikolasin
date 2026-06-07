from django.db import models
from ckeditor.fields import RichTextField

class Vest(models.Model):

    naslov = models.CharField(max_length=100)
    opis = models.CharField(max_length=255)

    image = models.ImageField(upload_to='images/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name_plural = 'Vesti'


class Video(models.Model):

    naslov = models.CharField(max_length=100)

    opis = models.CharField(max_length=500)

    video = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_url(self):

        if "watch?v=" in self.video:
            video_id = self.video.split("watch?v=")[1].split("&")[0]

            return f"https://www.youtube.com/embed/{video_id}"

        return self.video

    def __str__(self):
        return self.naslov


class Rec(models.Model):

    naslov = models.CharField(max_length=255)

    autor = models.CharField(max_length=255)

    slika = models.ImageField(upload_to='rec/')

    paragraf1 = models.TextField()
    paragraf2 = models.TextField()
    citat = models.CharField(max_length=100)
    paragraf3 = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.naslov


class Film(models.Model):
    TAG_CHOICES = [
        ('premijera', 'Премијера'),
        ('klasik', 'Класик'),
        ('domaci', 'Домаћи филм'),
        ('strani', 'Страни филм'),
        ('uskoro', 'Ускоро'),
        ('poseban', 'Посебна пројекција'),
    ]

    title = models.CharField(max_length=255, verbose_name='Назив филма')
    description = models.TextField(verbose_name='Опис')
    image = models.ImageField(upload_to='bioskop/', verbose_name='Постер')
    screening_date = models.DateTimeField(verbose_name='Датум и вријеме пројекције')
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена карте')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True, verbose_name='Ознака')
    featured = models.BooleanField(default=False, verbose_name='Истакнути филм')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Filmovi'
        ordering = ['screening_date']


class Artwork(models.Model):
    author_name = models.CharField(max_length=255, verbose_name='Ime autora')
    title = models.CharField(max_length=255, verbose_name='Naziv slike')
    description = models.TextField(verbose_name='Opis slike')
    image = models.ImageField(upload_to='likovna-kolonija/')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(f"{self.author_name}-{self.title}")
            slug = base
            n = 1
            while Artwork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author_name} — {self.title}"

    class Meta:
        verbose_name_plural = 'Likovna kolonija — slike'
        ordering = ['-created_at']
