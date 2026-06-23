python -m PyInstaller --onefile --windowed --name Casino --distpath dist --workpath build --add-data "assets;assets" --noupx --clean --noconfirm main.py

что означают параметры:
python -m PyInstaller - запускает сборщик PyInstaller
main.py - главный файл, с которого запускается проект
--onefile - упаковывает программу и зависимости в один EXE
--windowed - не показывает чёрную консоль вместе с приложением
--name Casino - создаёт файл с именем Casino.exe
--distpath dist - помещает готовый EXE в папку dist
--workpath build - использует папку build для временных файлов сборки
--add-data "assets;assets" - добавляет папку assets со звуком внутрь приложения
--noupx - отключает дополнительное сжатие библиотек, которое вызывало ошибку с libmpv-2.dll
--clean - очищает кэш старых сборок
--noconfirm - автоматически разрешает перезаписать предыдущую сборку

casino/
build/ - временные файлы сборки
dist/
Casino.exe - готовая программа
Casino.spec - конфигурация сборки PyInstaller