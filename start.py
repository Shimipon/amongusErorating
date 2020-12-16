import sqlite3

def main():
	conn = sqlite3.connect('PlayerList.db')
	c = conn.cursor()
	c.execute("CREATE TABLE Players (name TEXT PRIMARY KEY, im INTEGER, cr INTEGER)")
	conn.commit()
	conn.close()

if __name__ == "__main__":
    main()