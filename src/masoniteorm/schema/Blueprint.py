from .Table import Table


class Blueprint:
    """Used for building schemas for creating, modifying or altering schema."""

    def __init__(
        self,
        grammar,
        table="",
        connection=None,
        platform=None,
        action=None,
        default_string_length=None,
        dry=False,
    ):
        self.grammar = grammar
        self.table = table
        self._last_column = None
        self._default_string_length = default_string_length
        self.platform = platform
        self._dry = dry
        self._action = action
        self.connection = connection
        if not platform:
            self.platform = self.connection.get_default_platform()

    def string(self, column, length=255, nullable=False):
        """Sets a column to be the string representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            length {int} -- The length of the column. (default: {255})
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "string", length=length, nullable=nullable
        )

        return self

    def integer(self, column, length=11, nullable=False):
        """Sets a column to be the integer representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            length {int} -- The length of the column. (default: {255})
            nullable {bool} -- Whether the column is nullable (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "integer", length=length, nullable=nullable
        )
        return self

    def _compile_create(self):
        return self.grammar(creates=self._columns, table=self.table)._compile_create()

    def _compile_alter(self):
        return self.grammar(creates=self._columns, table=self.table)._compile_create()

    def increments(self, column, nullable=False):
        """Sets a column to be the auto incrementing primary key representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "increments", nullable=nullable
        )
        return self

    def big_increments(self, column, nullable=False):
        """Sets a column to be the the big integer increments representation for the table

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "big_increments", nullable=nullable
        )
        return self

    def binary(self, column, nullable=False):
        """Sets a column to be the binary representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(column, "binary", nullable=nullable)
        return self

    def boolean(self, column, nullable=False):
        """Sets a column to be the boolean representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(column, "boolean", nullable=nullable)
        return self

    def default(self, value):
        self._last_column.default = value
        return self

    def char(self, column, length=1, nullable=False):
        """Sets a column to be the char representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            length {int} -- The length for the column (default: {1})
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "char", length=length, nullable=nullable
        )
        return self

    def date(self, column, nullable=False):
        """Sets a column to be the date representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(column, "date", nullable=nullable)
        return self

    def datetime(self, column, nullable=False):
        """Sets a column to be the datetime representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(column, "datetime", nullable=nullable)
        return self

    def timestamp(self, column, nullable=False, now=None):
        """Sets a column to be the timestamp representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})
            now {bool} -- Whether the default for the column should be the current time. (default: {False})

        Returns:
            self
        """
        if now:
            now = "now"

        self._last_column = self.table.add_column(
            column, "timestamp", nullable=nullable
        )

        if not now:
            self._last_column.use_current()

        return self

    def timestamps(self):
        """Creates `created_at` and `updated_at` timestamp columns.

        Returns:
            self
        """
        self.table.add_column("created_at", "timestamp", nullable=False).use_current()

        self.table.add_column("updated_at", "timestamp", nullable=False).use_current()

        return self

    def decimal(self, column, length=17, precision=6, nullable=False):
        """Sets a column to be the decimal representation for the table.

        Arguments:
            column {string} -- The name of the column.

        Keyword Arguments:
            length {int} -- The total length of the decimal number (default: {17})
            precision {int} -- The number of places that should be used for floating numbers. (default: {6})
            nullable {bool} -- Whether the column is nullable (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "decimal", length=(length, precision), nullable=nullable
        )
        return self

    def double(self, column, nullable=False):
        """Sets a column to be the the double representation for the table

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(column, "double", nullable=nullable)
        return self

    def enum(self, column, options=[], nullable=False):
        """Sets a column to be the enum representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            options {list} -- A list of available options for the enum. (default: {False})
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        new_options = ""
        for option in options:
            new_options += "'{}',".format(option)
        new_options = new_options.rstrip(",")
        self._last_column = self.table.add_column(
            column, "enum", length=new_options, nullable=nullable
        )
        return self

    def text(self, column, length=None, nullable=False):
        """Sets a column to be the text representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            length {int} -- The length of the column if any. (default: {False})
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "text", length=length, nullable=nullable
        )
        return self

    def unsigned(self, column=None, length=None, nullable=False):
        """Sets a column to be the unsigned integer representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            length {int} -- The length of the column. (default: {False})
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        if not column:
            self._last_column.column_type = "unsigned_integer"
            self._last_column.length = None
            return self

        self._last_column = self.table.add_column(
            column, "unsigned", length=length, nullable=nullable
        )
        return self

    def unsigned_integer(self, column, nullable=False):
        """Sets a column to be the unsigned integer representation for the table.

        Arguments:
            column {string} -- The column name.

        Keyword Arguments:
            nullable {bool} -- Whether the column is nullable. (default: {False})

        Returns:
            self
        """
        self._last_column = self.table.add_column(
            column, "unsigned_integer", nullable=nullable
        )
        return self

    def to_sql(self):
        """Compiles the blueprint class into a sql statement.

        Returns:
            string -- The SQL statement generated.
        """
        if self._action == "create":
            return self.platform().compile_create_sql(self.table)
        else:
            return self.platform().compile_alter_sql(self.table)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._dry:
            return

        return self.connection.query(self.to_sql(), ())

    def nullable(self):
        """Sets the last column created as nullable

        Returns:
            self
        """
        self._last_column.nullable()
        return self

    def soft_deletes(self, name="deleted_at"):
        return self.datetime(name, nullable=True).nullable()

    def unique(self, column=None):
        """Sets the last column to be unique if no column name is passed.

        If a column name is passed this method will create a new unique column.

        Keyword Arguments:
            column {string} -- The name of the column. (default: {None})

        Returns:
            self
        """
        if column is None:
            self.table.add_constraint(
                self._last_column.name, "unique", columns=[self._last_column.name]
            )
            return self

        self.table.add_constraint(column, "unique", columns=[column])

        return self

    def index(self, column):
        """Creates a constraint based on the index constraint representation of the table.

        Arguments:
            column {string} -- The name of the column to create the index on.

        Returns:
            self
        """
        self.table.add_constraint(column, "index")
        return self

    def fulltext(self, column):
        """Creates a constraint based on the full text constraint representation of the table.

        Arguments:
            column {string} -- The name of the column to create the index on.

        Returns:
            self
        """
        self.table.add_constraint(column, "fulltext")
        return self

    def primary(self, column):
        """Creates a constraint based on the primary key constraint representation of the table.

        Arguments:
            column {string} -- The name of the column to create the index on.

        Returns:
            self
        """
        self.table.set_primary_key([column])
        return self

    def foreign(self, column):
        """Starts the creation of a foreign key constraint

        Arguments:
            column {string} -- The name of the column to create the index on.

        Returns:
            self
        """
        self._last_foreign = self.table.add_foreign_key(column)
        return self

    def references(self, column):
        """Sets the other column on the foreign table that the local column will use to reference.

        Arguments:
            column {string} -- The name of the column to create the index on.

        Returns:
            self
        """
        self._last_foreign.references(column)
        return self

    def on(self, table):
        """Sets the foreign table that the local column will use to reference on.

        Arguments:
            table {string} -- The foreign table name.

        Returns:
            self
        """
        self._last_foreign.on(table)
        return self

    def on_delete(self, action):
        """Sets the last foreign key to a specific on delete action.

        Arguments:
            action {string} -- The specific action to do on delete.

        Returns:
            self
        """
        self._last_foreign.on_delete(action)
        return self

    def on_update(self, action):
        """Sets the last foreign key to a specific on update action.

        Arguments:
            action {string} -- The specific action to do on update.

        Returns:
            self
        """
        self._last_foreign.on_update(action)
        return self

    def rename(self, old_column, new_column, data_type):
        """Rename a column from the old value to a new value.

        Arguments:
            old_column {string} -- The name of the original old column name.
            new_column {string} -- The name of the new column name.

        Returns:
            self
        """
        self.table.rename_column(old_column, new_column, data_type)
        return self

    def after(self, old_column):
        """Sets the column that this new column should be created after.

        This is useful for setting the location of the new column in the table schema.

        Arguments:
            old_column {string} -- The column that this new column should be created after

        Returns:
            self
        """
        self._last_column.after(old_column)
        return self

    def drop_column(self, *columns):
        """Sets columns that should be dropped

        Returns:
            self
        """
        for column in columns:
            self.table.drop_column(column)

        return self

    def drop_index(self, indexes):
        """Specifies indexes that should be dropped.

        Arguments:
            indexes {list|string} -- Either a list of indexes or a specific index.

        Returns:
            self
        """
        if isinstance(indexes, str):
            indexes = [indexes]

        for index in indexes:
            # self._last_column = self.new_column(
            #     None, index, None, None, action="drop_index"
            # )
            # self._columns += (self._last_column,)
            self._constraints += (
                Constraint(index, constraint_type="index", action="drop"),
            )
        return self

    def drop_unique(self, indexes):
        """Drops a unique index.

        Arguments:
            indexes {list|string} -- Either a list of indexes or a specific index.

        Returns:
            self
        """
        if isinstance(indexes, str):
            indexes = [indexes]

        for index in indexes:
            # self._last_column = self.new_column(
            #     None, index, None, None, action="drop_unique"
            # )
            self._constraints += (
                Constraint(index, constraint_type="unique", action="drop"),
            )
        return self

    def drop_primary(self, index=""):
        """Drops a primary key index.

        Returns:
            self
        """
        # self._last_column = self.new_column(
        #     None, None, None, None, action="drop_primary"
        # )

        index = self.grammar().primary_key_string().format(table=self.table)
        self._constraints += (
            Constraint(index, constraint_type="primary", action="drop"),
        )
        # self._columns += (self._last_column,)
        return self

    def drop_foreign(self, indexes):
        """Drops foreign key indexes.

        Arguments:
            indexes {list|string} -- Either a list of indexes or a specific index.

        Returns:
            self
        """
        if isinstance(indexes, str):
            indexes = [indexes]

        for index in indexes:
            if not index.startswith(self.table):
                index = self.table + "_" + index
            if not index.endswith("foreign"):
                index = index + "_foreign"

            # self._last_column = self.new_column(
            #     None, key, None, None, action="drop_foreign"
            # )
            # self._last_column.is_constraint = True
            self._constraints += (
                Constraint(index, constraint_type="foreign", action="drop"),
            )
        return self
