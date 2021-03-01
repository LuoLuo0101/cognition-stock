
class empty:
    pass


class Field(object):
    default_error_messages = {
        'required': 'This field is required.',
        'null': 'This field may not be null.'
    }

    def __init__(self, read_only=False, write_only=False, required=None, default=empty, source=None,
                 label=None, help_text=None, error_messages=None, allow_null=False):
        self.read_only = read_only
        self.write_only = write_only
        self.required = required
        self.default = default  # 如果没有指定，那么给一个默认值
        self.source = source  # 对应ORM中的表字段
        self.label = label  # 显示在
        self.help_text = help_text  # 提示文本
        self.allow_null = allow_null  # 允许为空
        messages = {}
        for cls in reversed(self.__class__.__mro__):
            messages.update(getattr(cls, 'default_error_messages', {}))
        messages.update(error_messages or {})
        self.error_messages = messages


class CharField(Field):
    default_error_messages = {
        'invalid': 'Not a valid string.',
        'blank': 'This field may not be blank.',
        'max_length': 'Ensure this field has no more than {max_length} characters.',
        'min_length': 'Ensure this field has at least {min_length} characters.',
    }

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)  # 去掉字段前后空格
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)
        super(CharField, self).__init__(**kwargs)


class EmailField(Field):
    pass


class UUIDField(Field):
    pass


class IPAddressField(Field):
    pass


class IntegerField(Field):
    pass


class FloatField(Field):
    pass


class DecimalField(Field):
    pass


class DateTimeField(Field):
    pass


class DateField(Field):
    pass


class TimeField(Field):
    pass


class ChoiceField(Field):
    pass


class MultipleChoiceField(Field):
    pass


class JSONField(Field):
    pass

