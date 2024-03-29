from config.settings import ROOT_DIR, TABLE_NAME

with open(f"{ROOT_DIR}/init.sql", "r") as f:
    init_sql = f.read()

init_sql = init_sql.replace("${TABLE_NAME}", TABLE_NAME)

with open(f"{ROOT_DIR}/init.sql", "w") as f:
    f.write(init_sql)
