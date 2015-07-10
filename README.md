# botgram
Create your own module and run the telegram bot!

### Desc
It is very easy to extend the module and create your own command for this telegram bot. Do not forget to set your own token in the config file. Also set your bot username to the config file, to verify the command when there are two or more robots in one group.
Just create your module, put it into mod folder, and register it in the config file. And also, you have to install mongodb first, because the script need mongodb for logging the previous message and command that you have executed.

### Requirement
First:

- Mongodb

```sh
$ sudo pip install -r requirements.txt
```

### How to
If you want to add new module, please see ipinfo module for the sample. After that, just run botgram every 5 / 10 / 15 / whatever seconds that you want to.

```sh
$ python botgram.py
```

### Command List
Just send /help to your chatbot

![alt tag](http://blog.bermain.net/tele_bot.png)
