# kivymd_reload_async
A demo [KivyMD](https://kivymd.readthedocs.io/en/latest/) resource-based application showcasing:
* Hot reload (using native KivyMD calls rather than Kaki) 
* Asynchronous IO using [Trio](https://trio.readthedocs.io/en/stable/)

Forked from [JennaSys/kivy_rest](https://github.com/JennaSys/kivy_rest)

## Usage

```
poetry install
poetry run ptw # Exception ignored in: functools.partial(<function _widget_destructor at 0x1054ec8b0>, 63)
poetry run python3 kivymd_reload_async/main.py
```
