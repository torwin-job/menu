from django import template
from django.urls import resolve
from django.utils.safestring import mark_safe
from django.conf import settings

from tree_menu.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    
    try:
        current_url_name = resolve(current_path).url_name
    except:
        current_url_name = ''
    
    try:
        # Один запрос к БД для получения меню и всех его пунктов
        menu = Menu.objects.get(name=menu_name)
        menu_items = MenuItem.objects.filter(menu=menu).select_related('parent')
        
        # Строим дерево пунктов меню
        menu_tree = {}
        root_items = []
        
        for item in menu_items:
            item.children_items = []
            menu_tree[item.id] = item
            
            if item.parent_id is None:
                root_items.append(item)
        
        # Связываем родителей и детей
        for item in menu_items:
            if item.parent_id is not None and item.parent_id in menu_tree:
                menu_tree[item.parent_id].children_items.append(item)
        
        # Определяем активные элементы
        active_item_ids = set()
        for item in menu_items:
            url = item.get_url()
            if url == current_path or (item.named_url and item.named_url == current_url_name):
                active_id = item.id
                # Добавляем все родительские элементы в активные
                while active_id:
                    active_item_ids.add(active_id)
                    parent_id = menu_tree.get(active_id).parent_id
                    active_id = parent_id
        
        # Рендерим меню
        result = '<ul class="menu">'
        
        def render_menu_items(items, level=0):
            result = ''
            for item in items:
                is_active = item.id in active_item_ids
                has_children = len(item.children_items) > 0
                
                css_class = 'menu-item'
                if is_active:
                    css_class += ' active'
                
                result += f'<li class="{css_class}">'
                result += f'<a href="{item.get_url()}">{item.name}</a>'
                
                # Разворачиваем пункт, если он активен или его родитель активен
                if has_children and (is_active or level == 0 or 
                                    (item.parent_id in active_item_ids and level == 1)):
                    result += '<ul class="submenu">'
                    result += render_menu_items(sorted(item.children_items, key=lambda x: x.order), level + 1)
                    result += '</ul>'
                
                result += '</li>'
            return result
        
        result += render_menu_items(sorted(root_items, key=lambda x: x.order))
        result += '</ul>'
        
        return mark_safe(result)
    except Menu.DoesNotExist:
        return ''
    except Exception as e:
        if settings.DEBUG:
            return mark_safe(f'<div class="error">Error rendering menu: {str(e)}</div>')
        return '' 