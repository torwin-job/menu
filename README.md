# Django Tree Menu

Приложение Django для создания древовидных меню с возможностью управления через админку.

## Особенности

- Меню реализовано через template tag
- Все пункты над выделенным пунктом развернуты, а также первый уровень вложенности под выделенным пунктом
- Меню хранится в БД и редактируется в стандартной админке Django
- Активный пункт меню определяется исходя из URL текущей страницы
- На одной странице может быть несколько меню, определяемых по названию
- При клике на меню происходит переход по заданному URL (явному или named URL)
- На отрисовку каждого меню требуется ровно 1 запрос к БД

## Установка

1. Клонировать репозиторий
2. Создать и активировать виртуальное окружение
3. Установить зависимости: `pip install django`
4. Применить миграции: `python manage.py migrate`
5. Создать суперпользователя: `python manage.py createsuperuser`
6. Запустить сервер: `python manage.py runserver`

## Использование

1. Войдите в админку Django по адресу `/admin/` и создайте меню с пунктами
2. Используйте template tag для отображения меню в шаблонах:

```html
{% load menu_tags %}
{% draw_menu 'main_menu' %}
```

## Работа с админ-панелью

### Создание меню

1. Войдите в админ-панель Django по адресу `/admin/`
2. Перейдите в раздел "Меню" и нажмите "Добавить меню"
3. Введите название меню - это важно! Именно это название будет использоваться в шаблонах для отображения меню
4. Например, если вы создали меню с названием `main_menu`, то в шаблоне вызывайте его как `{% draw_menu 'main_menu' %}`
5. Сохраните меню

### Добавление пунктов меню

1. В админ-панели можно добавлять пункты меню двумя способами:
   - Через встроенную форму при создании/редактировании меню
   - Через отдельный раздел "Пункты меню"

2. Для каждого пункта меню необходимо указать:
   - Название пункта (отображается в меню)
   - Меню, к которому относится пункт
   - Родительский пункт (если это подпункт)
   - URL (прямая ссылка) или Named URL (имя URL-маршрута)
   - Порядок (для сортировки пунктов)

3. Для создания иерархической структуры:
   - Сначала создайте родительский пункт
   - Затем создайте дочерние пункты, указав родительский пункт в поле "Родительский пункт"

### Настройка URL

В пункте меню можно указать URL одним из двух способов:

1. **Прямой URL** - указывается в поле "URL", например: `/about/`, `/services/`
2. **Named URL** - указывается в поле "Named URL", например: `tree_menu:about`, `tree_menu:services`

Если указаны оба поля, приоритет имеет прямой URL.

### Примеры названий меню

Вы можете создать несколько меню с разными названиями и использовать их на разных страницах:

- `main_menu` - главное меню сайта
- `footer_menu` - меню в подвале сайта
- `sidebar_menu` - боковое меню
- `user_menu` - меню пользователя

Затем в шаблонах вызывайте нужное меню по его названию:

```html
{% load menu_tags %}
{% draw_menu 'main_menu' %}
{% draw_menu 'footer_menu' %}
```

## Структура проекта

- `tree_menu/models.py` - модели для меню и пунктов меню
- `tree_menu/admin.py` - настройки админки
- `tree_menu/templatetags/menu_tags.py` - template tag для отрисовки меню
- `tree_menu/templates/` - шаблоны для примера использования

## Примеры

В проекте есть пример использования меню, доступный по корневому URL (`/`). 