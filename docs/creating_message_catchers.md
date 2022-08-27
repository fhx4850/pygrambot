## Creating message catchers

Two handlers can be used to catch user messages, namely ```CatchNextMessage``` and ```CatchMultipleMessages```.

```CatchNextMessage``` - catches one message and aborts.

```CatchMultipleMessages``` - Catches several messages until a stop command is received. 
To stop the handler, stop commands must be specified using the ```add_stop_commands``` method.

To create a handler, you need to inherit from one of the base classes. After that, you need to implement the ```handle``` method.

**Code example**
```
from pygrambot.bot.bothandlers.handlers import CatchMultipleMessages, CatchNextMessage

class ProcessingCatchMsg(CatchNextMessage):
    async def handle(self, updatedt):
        print(updatedt.message.text)


class CatchMultMsg(CatchMultipleMessages):
    async def handle(self, updatedt):
        await SendCommand(TOKEN).sendMessage(updatedt.chat.id, updatedt.message.text)
```
You can now launch and use handlers using commands.

**Below is an example of using these handlers in bot commands**
```
from _mybot.handlers import ProcessingCatchMsg, CatchMultMsg

class CatchMsg(NewCommand):
    command = 'catch'
    handler = ProcessingCatchMsg


class Test(NewCommand):
    command = 'm_catch'
    handler = CatchMultMsg.add_stop_commands(['stop'])
```