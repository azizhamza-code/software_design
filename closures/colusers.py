class NotInTheClass(Exception):
    pass

class NotSameType(Exception):
    pass




def make_object(initial_value, **kwargs):
    private = {"value": initial_value}
    private.update(kwargs)

    def getter(name='value'):
        if name not in private:
            raise NotInTheClass(f"{name} not in the class")
        return private[name]

    def setter(new_value, name='value'):
        if type(new_value) != type( private[name]):
            raise NotSameType(f"{private[name]}    not the same type {new_value}")
        private[name] = new_value

    return {"get": getter, "set": setter}

object = make_object(00)
print("initial value", object["get"]())
object["set"](99)
print("object now contains", object["get"]())


if __name__ == '__main__':
    f = make_object(3, a= 4)
    print( f"a= { f['get']('a')}")
    print( f" { f['set']('5', 'a')}")
    print( f"a= { f['get']('value')}")
    print( f"a= { f['get']('f')}")