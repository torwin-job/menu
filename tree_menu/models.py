from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название меню')
    
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items', verbose_name='Меню')
    name = models.CharField(max_length=100, verbose_name='Название пункта')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='Родительский пункт')
    url = models.CharField(max_length=255, verbose_name='URL', blank=True)
    named_url = models.CharField(max_length=255, verbose_name='Named URL', blank=True)
    order = models.IntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_url(self):
        if self.url:
            return self.url
        elif self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return '#'
        return '#'
