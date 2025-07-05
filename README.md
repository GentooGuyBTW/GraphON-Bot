[![Build with Nuitka](https://github.com/GentooGuyBTW/GraphON-Bot/actions/workflows/build.yml/badge.svg)](https://github.com/GentooGuyBTW/GraphON-Bot/actions/workflows/build.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# GraphON-Bot
## Поддерживаемые платформы: Windows, Linux, Mac OS.

# Инструкция по установке:
## Запуск бинарника (рекомендуется):
### GraphON-Bot скомпилирован под 3 платформы. Исполняемые находятся в разделе "Releases", либо в результатах работы GitHub Actions.
## Ручная (для особых случаев):
```
git clone https://github.com/GentooGuyBTW/GraphON-Bot.git
cd GraphON-Bot
pip install -r requirements.txt
python main.py
```
## Настройка .env
### Для работы бота необходимо настроить .env, который должен находиться в одной директории с ботом.
### Структура .env:
```
BOT_TOKEN=[TOKEN]
CHAT_ID=[ID]
```