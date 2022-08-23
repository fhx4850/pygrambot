## Create project

---

First you need to create a python file (in this example, there will be a ```main.py``` file) and write the following code in it:
```
from pygrambot.cli import bot_cli
```
Bot console commands are now available. To create bot configuration files, run the following command:
```
python3 main.py init
```
The config directory has now been created in the root directory of the project, which contains the configuration files. For the minimum performance of the bot, you need to specify your own bot token.
To start the bot, you need to enter the command:
```
python3 main.py start
```


To add bot functionality, you need to create a ```commands.py``` file and add the **path to the folder** with the file in ```RELATIVE_PATH_TO_COMMANDS``` (config) variable, then create a file with handlers (in this example, the ```handlers.py``` file).

```commands.py``` - a file that contains all the commands for the bot.
```handlers.py``` - file that contains custom handlers.

**Code Example**:

```
TOKEN = ''
RELATIVE_PATH_TO_COMMANDS = [test_bot/]
RELATIVE_PATH_TO_MIDDLEWARES = []
```

---

#### *Create command*

To create a command, you need to create a class and inherit from the ```NewCommand``` class(```from pygrambot.bot.botcommands.commands import NewCommand```). Next, you need to set the values ​​for the following variables:

* **command** - the name of the command to call it. 
* **description** - short description of the command.
* **handler** - the handler that is executed when the cosanda starts.

> **NOTE**
> 
> In order for the command to respond to all messages, you need to give it the name "*". No description is required for such a command.

**Code Example**:

```
from pygrambot.bot.botcommands.commands import NewCommand

class StartCommand(NewCommand):
    command = 'start'
    description = 'start bot'
    handler = StartHandler
```

---

#### *Create handler*

To create a command handler, you need to create a class and inherit from the CustomHandler class (```from pygrambot.bot.bothandlers.handlers import CustomHandler```). After that, you need to implement the ```start``` method.

> **NOTE**
> 
> If a built-in handler is used, you need to inherit from it and implement the **```handle```** method, not **```start```**.

**Code Example**:

```
from pygrambot.bot.bothandlers.handlers import CustomHandler

class StartHandler(CustomHandler):

    async def start(self):
        await SendCommand(TOKEN).sendMessage(self.updatedt.chat.id, 'Hello!')
```
---

*This manual describes the basic principles of this framework, all work will be based on these principles.*