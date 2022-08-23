## Built-in data types

---

**UpdateDt** - the data type that provides the result of the telegram api command ```getUpdates```.

**Object fields**:
* ```update_id``` - The ID of the current update.
* ```message``` - Message Information.
    
    The message class currently contains the following fields:
    * date
    * text
    * message_id
    * id
    * is_bot
    * first_name
    * username
    * language_cod

* ```chat``` - Information about the current chat.

    The chat class currently contains the following fields:
    * id
    * first_name
    * username
    * type

* ```data``` - a field that contains arbitrary user data in a dictionary format.

> **NOTE**
> 
> The fields in the message and chat classes are dynamically created using the **setattr()** function depending on the result returned by the getUpdates command.

---

**BotCommandDt** - an object that contains information about the command.

**Object fields**:
* ```command``` - command name.
* ```description``` - command description.