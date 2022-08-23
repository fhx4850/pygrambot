## Create middlewares

---

**Middleware** (in this framework) is software that is called (in order) every day before executing a command and can change the initial data, execute custom logic, block command execution, and much more.

To create a middleware, you need to import the ```NewMiddleware``` class (```from pygrambot.bot.middlewares import NewMiddleware```) and implement the ```run``` method. The method must always return the data type [UpdateDt](https://github.com/uwine4850/pygrambot/tree/master/docs/data_objects.md). 
Next, you need to add the **path to the middleware folder** to ```RELATIVE_PATH_TO_MIDDLEWARES```(conf).

**Code Example**:

```
TOKEN = ''
RELATIVE_PATH_TO_COMMANDS = [test_bot/]
RELATIVE_PATH_TO_MIDDLEWARES = [test_bot/middlewares/]
```

> **NOTE**
> 
> Middleware class methods must be static. To do this, you need to use the **```@classmethod```** decorator.

**Code Example**:

```
from pygrambot.bot.middlewares import NewMiddleware

class Test(NewMiddleware):
    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        # code
        return updatedt
```

After creating the middlewares, you need to create a list called ```middlewareslist``` and add a link to the middlewares to it.

**Code Example**:

```
middlewareslist = [
    Test,
]
```

In addition to your own middlewares, you can use built-in ones, for example, in the ```pygrambot.bot.middlewares``` module there is ```ThrottlingMiddleware```. To use it, add the class to ```middlewareslist```. Built-in middlewares are configurable.