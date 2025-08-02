from django.utils.text import slugify
from django.db import models

class SlugTitleSaver(models.Model):
    slug_source_field = 'name'
    
    def save(self, *args, **kwargs):
        source_fields = getattr(self, 'slug_source_field', None)
        if source_fields:
            if isinstance(source_fields, list):
                source_value = '-'.join(str(getattr(self, f, '')) for f in source_fields)
            else:
                source_value = str(getattr(self, source_fields, ''))
            self.slug = slugify(source_value)
        super().save(*args, **kwargs)
    class Meta:
        abstract = True