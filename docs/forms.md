## Create Forms

Forms are designed to easily receive specific information from the user and process it. The form is launched using a 
regular command and processed by a special built-in handler.

Before creating a form, you need to create a [command for it](https://github.com/uwine4850/pygrambot/blob/master/docs/create_project.md).
After that, you need to inherit from the built-in ```Form Handler``` handler, fill in the ```fields``` class variable 
and implement the ```handle``` method.

**Code example:**

*commads.py*
```
from pygrambot.bot.botcommands.commands import NewCommand
from _mybot.handlers import TestFormHandler

class FormCommand(NewCommand):
    command = 'form'
    description = 'command description'
    handler = TestFormHandler
```
*handlers.py*
```
from pygrambot.bot.bothandlers.handlers import FormHandler

class TestFormHandler(FormHandler):
    fields = ['field1', 'field2']
    
    async def handle(updatedt):
        print(updatedt.data['form'])
```

The form data is stored in the ```data``` variable of the ```updated``` class. The data under the ```form``` key.