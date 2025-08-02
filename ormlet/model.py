from .column import Column


class Model:
    @classmethod
    def get_table_schema(cls):
        table_name = cls.get_table_name()
        schema = f"CREATE TABLE IF NOT EXISTS '{table_name}' ("
        columns = cls.get_columns()
        schema += ", ".join([columns[key]._to_sql() for key in columns.keys()]) + ");"

        return schema

    @classmethod
    def get_table_name(cls) -> str:
        if hasattr(cls, "__table__"):
            table_name = cls.__table__.lower()
        else:
            table_name = cls.__name__.lower()

        return table_name

    @classmethod
    def get_columns(cls):
        columns = {}
        for key, value in cls.__dict__.items():
            if isinstance(value, Column):
                value.field_name = key
                columns[key] = value

        return columns

    @classmethod
    def get_primary_field(cls):
        for _, value in cls.__dict__.items():
            if isinstance(value, Column):
                if value.primary_key:
                    return value

    def __repr__(self):
        attrs = [a for a in vars(self).keys()][:2]
        attr_str = ", ".join(f"{a}={getattr(self, a, 'N/A')}" for a in attrs)
        return f"<{self.__class__.__name__} {attr_str}>"
