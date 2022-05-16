from globalTypes import *

# Procedure st_insert inserts line numbers and
# memory locations into the symbol table
# loc = memory location is inserted only the
# first time, otherwise ignored
def st_insert(t, tables, cur):
    if t.name in tables[cur]:
        tables[cur][t.name]['type'] = t.type
    else:
        tables[cur][t.name] = {'lineno': t.lineno, 'type': t.type}
    if t.type == ExpType.Array:
        tables[cur][t.name]['size'] = t.size
# Function st_lookup returns the memory
# location of a variable or -1 if not found
def st_lookup(name, table):
    if name in table:
        return table[name]['lineno']
    return -1

def st_global_lookup(name, prev_table, tables):
    for i in range(prev_table, -1, -1):
        if st_lookup(name, tables[prev_table]):
            return True
    return -1

# Procedure printSymTab prints a formatted
# listing of the symbol table contents
# to the listing file
def printSymTables(tables):
    for table in tables:
        print("Variable Name  Line No.    Attributes")
        print("-------------  --------   ------------")
        for key, value in table.items():
            print(f"{key:14}{value['lineno']:2d}", end='')
            print(' '*9, value['type'])
        print('\n')
