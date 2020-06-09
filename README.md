# AMYR Python Self Bot
This is a funny telegram script that destributed by [Telethon](https://github.com/LonamiWebs/Telethon) python library.
You can login this bot by your original telegram account and use fun commands.

---
Commands:
  - !selfhelp
  - !me
  - !animchar [loop] [char]
  - !heart [loop]
  - !id [reply]
  - !stats
  - And other fun commands....

### Installation (Ubuntu)

First, you must install clone this repository in your directory:
```sh
$ cd ~
$ git clone https://github.com/4myr/self-bot
$ cd self-bot
```

Then, please install python3 and telethon library by pip3
```sh
$ sudo apt update
$ sudo apt install python3 screen
$ pip3 install telethon
$ cd self-bot
```

Now, you have to edit `config.py` file by `nano config.py` 
Enter your API KEY & API HASH between quotes

Now you can start and login bot
```sh
$ screen python3 bot.py
```

For first time you must login your account and for next times you don't need to it.
You can use `CTRL + A + D` for deatach screen.
