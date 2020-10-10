from .Column import Column


class TableDiff:
    def __init__(self, name):
        self.name = name
        self.from_table = None
        self.new_name = None
        self.removed_indexes = {}
        self.added_columns = {}
        self.dropped_columns = []
        self.renamed_columns = {}
        self.removed_constraints = {}
        self.added_constraints = {}
        self.added_foreign_keys = {}

    def from_table(self, from_table):
        self.from_table = from_table

    def remove_constraint(self, name):
        self.removed_constraints.update({name: self.from_table.get_constraint(name)})

    def get_removed_constraints(self):
        return self.removed_constraints

    def add_column(
        self, name=None, column_type=None, length=None, nullable=False, default=None
    ):
        self.added_columns.update({name: Column(name, column_type)})
        return self

    def get_added_columns(self):
        return self.added_columns

    def rename_column(
        self,
        original_name,
        new_name,
        column_type=None,
        length=None,
        nullable=False,
        default=None,
    ):
        self.renamed_columns.update(
            {
                original_name: Column(
                    new_name,
                    column_type,
                    length=length,
                    nullable=nullable,
                    default=default,
                )
            }
        )

    def remove_index(self, name):
        self.removed_indexes.update({name: self.from_table.get_index(name)})

    def get_added_constraints(self):
        return self.added_constraints

    def add_foreign_key(self, column, table, foreign_column):
        self.added_foreign_keys.update(
            {column: ForeignKeyConstraint(column, table, foreign_column)}
        )

    def get_added_foreign_keys(self):
        return self.added_foreign_keys
    
    def drop_column(self, name):
        self.dropped_columns.append(name)

    def get_dropped_columns(self, name):
        self.dropped_columns.append(name)
