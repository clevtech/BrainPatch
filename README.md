# BrainPatch

Необходимо поставить xcode, homebrew, python3 и pip для работы системы:  

https://wsvincent.com/install-python3-mac/  

Потом надо поставить platformIO для mac os:  

https://docs.platformio.org/en/latest/ide/vscode.html#installation  

Потом надо поставить git:  

https://gist.github.com/derhuerst/1b15ff4652a867391f03  

Потом надо скопировать репозиторий, для этого откройте терминал и зайдите в папку, куда надо скопировать:  

```
cd FolderWhereToCopy
git clone https://github.com/clevtech/BrainPatch.git
```


Потом надо через pip3 установить все зависимости, для этого зайдите в терминал в папку куда скопировали:

```
cd FolderWhereToCopy/BrainPatch
sudo pip3 install -r requirements.txt
```

## Запуск программы
Потом делаем следующее:
1. Запускаем робота, он начинает раздавать сеть "BrainPatch" с паролем "brain", надо к ней подрубить комп
2. Запускаем считыватель и смотрим его порт, там должно быть что-то типа "/dev/tty.usbmodem5143", проверяется это с помощью команды в терминале "ls /dev/tty.usb*"
3. Списываем это значение в скрипт "test.py" в строку port на 17-ой строке
4. Запускаем test.py c помощью "python3 test.py"
5. Заходим в браузере на адрес "localhost:5000"
6. Как только запускается страница, компьютер начинает считывать данные с считывателя, и если челик усиленно думает, то отправляет на робота команду ехать
