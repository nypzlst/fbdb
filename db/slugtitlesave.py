from django.utils.text import slugify

class SlugTitleSaver:
    slug_source_field = 'name'
    
    def save(self, **kwargs):
        field = getattr(self,'slug_source_field','name')
        if hasattr(self,field):
            value = getattr(self, field)
            if isinstance(value,str):
                setattr(self,field,value.lower().title())
                self.slug = slugify(getattr(self,field))
        super().save(**kwargs)