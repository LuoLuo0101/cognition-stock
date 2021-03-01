from collections import OrderedDict

from sanic_serializer.fields import Field


class SerializerMetaclass(type):
    """
    This metaclass sets a dictionary named `_declared_fields` on the class.

    Any instances of `Field` included as attributes on either the class
    or on any of its superclasses will be include in the
    `_declared_fields` dictionary.
    """

    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]

        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = [
                    (field_name, obj) for field_name, obj
                    in base._declared_fields.items()
                    if field_name not in attrs
                ] + fields

        return OrderedDict(fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)


# @six.add_metaclass(SerializerMetaclass)
# class Serializer(object):
#
#     @property
#     def fields(self):
#         if not hasattr(self, '_fields'):
#             self._fields = BindingDict(self)
#             for key, value in self.get_fields().items():
#                 self._fields[key] = value
#         return self._fields
#
#     def run_validation(self, ):
#
#     def is_valid(self, raise_exception=False):
#         """
#         1. 验证 validate_ + field_name
#         """
#
#     def validate(self, attrs):
#         return attrs
