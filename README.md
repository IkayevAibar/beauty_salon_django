# Проект Beauty Salon (Django)

Этот проект создан на фреймворке Django (Python) и использует базу данных SQLite. Он предназначен для записи пользователей на услуги в салоне красоты.

## Что нужно для запуска

1. **Установленный Python 3.9 или выше** (чтобы провериться, откройте «Командную строку» или «PowerShell» в Windows и наберите `python --version`).
2. **Любой текстовый редактор** (для просмотра и изменения кода, например, Visual Studio Code).

## Как запустить проект

### 1. Скопировать проект (если вы ещё не скопировали)

1. Зайдите на страницу репозитория:

   [https://github.com/IkayevAibar/beauty_salon_django](https://github.com/IkayevAibar/beauty_salon_django)
2. Нажмите кнопку «Code» → «Download ZIP», сохраните архив на свой компьютер.
3. Распакуйте архив в удобную папку (например, `C:\projects\beauty_salon_django`).

Или, если вы умеете работать с Git, можете ввести в «Командной строке»:

`git clone https://github.com/IkayevAibar/beauty_salon_django.git`

### 2. Установить виртуальное окружение и активировать его

1. Откройте «Командную строку» или «PowerShell» и перейдите в папку с проектом. Пример в Windows:

   `cd C:\путь\к\проекту\beauty_salon_django`
2. Создайте виртуальное окружение (простыми словами, это «отдельная» версия Python для данного проекта). Введите:

   `python -m venv venv`
3. Активируйте окружение:

   * **Windows (PowerShell)** :

   `.\venv\Scripts\Activate.ps1`

   * **Windows (обычный cmd)** :

   `venv\Scripts\activate.bat`

   * **macOS/Linux** :

   `source venv/bin/activate`

После активации в начале строки должно появиться `(venv)`.

### 3. Установить необходимые пакеты

В папке проекта есть файл `req.txt` со списком всех нужных библиотек. Установите их командой:

`pip install -r req.txt`

Если всё пройдёт успешно, появится список «Successfully installed ...».

### 4. Настроить базу данных (SQLite уже включена)

В проекте используется файл базы данных `db.sqlite3`. Обычно он уже лежит в папке проекта. Если нужно, Django автоматически создаст недостающие таблицы. Для этого введите:

`python manage.py migrate`

После выполнения все нужные таблицы будут созданы (если их ещё не было).

### 5. Создать учётную запись администратора (необязательно, но полезно)

Если хотите попасть в встроенную админ-панель Django (адрес будет `/admin`), создайте суперпользователя:

`python manage.py createsuperuser`

Программа спросит имя пользователя, пароль и email (email можно не указывать).

### 6. Запустить сервер

Введите в той же консоли:

`python manage.py runserver`

Появится сообщение типа:

`Watching for file changes with StatReloader
Performing system checks...`

`Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.`

Это значит, что сайт запущен.

### 7. Открыть сайт

1. Откройте браузер (Chrome, Edge и т.п.).
2. Перейдите по адресу:

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — главная страница сайта.

   [http://127.0.0.1:8000/admin/]() — админ-панель Django.

### 8. Выключить сервер и виртуальное окружение (когда закончите)

* Нажмите в консоли `CTRL + C`, чтобы остановить сервер.
* Введите команду:

  `deactivate`

  чтобы выйти из виртуального окружения.

---

## Частые вопросы

1. **«Команда не найдена» или «Python не установлен»**

   Убедитесь, что у вас установлен Python 3.9 или выше и что он добавлен в PATH (при установке поставьте галочку «Add Python to PATH»).
2. **Проблемы с виртуальным окружением в Windows**

   Если появляется сообщение об ограничении запуска скриптов, выполните в PowerShell (один раз):

   `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

   Затем попробуйте снова активировать окружение.
3. **Занятый порт 8000**

   Если вдруг сервер говорит, что адрес уже занят, используйте другой порт:

   `python manage.py runserver 8080`

   Тогда сайт будет доступен по адресу: [http://127.0.0.1:8080/](http://127.0.0.1:8080/).
4. **Миграции**

   Если таблицы вдруг не создались или изменили структуру, выполните:

   `python manage.py makemigrations
   python manage.py migrate`

---

## Структура проекта (коротко)

<pre class="!overflow-visible" data-start="4525" data-end="5084"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none rounded-t-[5px]"></div><div class="sticky top-9"><div class="absolute bottom-0 right-0 flex h-9 items-center pr-2"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"></span><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre"><span><span>beauty_salon_django/
├── venv/               </span><span># Папка виртуального окружения (создаётся после python -m venv venv)</span><span>
├── beauty_salon/       </span><span># Папка с файлами Django-приложения</span><span>
│   ├─ settings.py      </span><span># Основные настройки</span><span>
│   ├─ urls.py          </span><span># Таблица маршрутов (какие адреса доступны)</span><span>
│   ├─ ...
├── salon/       	</span><span># Папка с файлами Салона</span><span>
│   ├─ admin.py    	</span><span># Настройка страницы админки</span><span>
│   ├─ urls.py          </span><span># Таблица маршрутов (какие адреса доступны)</span><span>
│   ├─ models.py        </span><span># Модели данных, которые представляют сущности в салоне красоты, такие как специалисты, услуги, бронирования и оценки.</span><span>
│   ├─ views.py         </span><span># Тут описаны весь функционал. Эти функции управляют регистрацией, входом в систему, выходом, просмотром и редактированием услуг, бронированиями, отзывами и статистикой. Они взаимодействуют с моделями данных и шаблонами для отображения информации пользователям.</span><span>
│   ├─ templates/salon  </span><span># Здесь находится все HTML страницы сайта</span><span>

├── db.sqlite3          </span><span># Файл базы данных SQLite (если вы его не удалили)</span><span>
├── req.txt             </span><span># Список всех необходимых библиотек Python</span><span>
├── manage.py           </span><span># Главная «управляющая» команда Django</span><span>
└── README.md           </span><span># Этот файл (инструкция)</span><span>
</span></span></code></div></div></pre>

---

## Лицензия и контакты

* Этот проект сделан в учебных целях.
* Если хотите что-то изменить или улучшить — создавайте «Pull Request» или пишите «Issue» в репозитории GitHub.

**Удачи с использованием проекта!**
