class Singleton(type):

    def __new__(cls, name, bases, attr_dict):
        cls_instances = {}

        def singleton_new(inner_cls):
            identity = id(inner_cls)

            if identity in cls_instances:
                return cls_instances[identity]
            else:
                # The parent class of the class `inner_cls` (1st argument) by traversing the `__mro__` of `inner_cls` (2nd argument)
                class_instance = super(inner_cls, inner_cls).__new__(inner_cls)
                class_instance.iter = 0

                class_instance.iter_registry = [{}]
                class_instance.kid_registry = {}
                cls_instances[identity] = class_instance
                return class_instance

        attr_dict['__new__'] = singleton_new

        singleton_instance = super().__new__(cls, name, bases, attr_dict)

        return singleton_instance
