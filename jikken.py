import RateMG
import random as rm
import sqlite3

def main():
	names = ["SA","SB","SC","SD","SE","SF","SG","SH","SI","SJ"]
	conn = sqlite3.connect('PlayerList.db')
	c = conn.cursor()
	for n in names:
		c.execute("DELETE FROM Players WHERE name = ? ", (n,))
		c.execute("INSERT INTO Players (name, im, cr) VALUES (?, ?, ?) ", (n, 1500, 1500,))
		conn.commit()
	conn.close()
	mg = RateMG.RateMG()
	for i in range(20):
		imp = rm.sample(names,2)
		crw = []
		for n in names:
			if not n in imp:
				crw.append(n)
		if "SA" in imp:
			if rm.randrange(10) < 6:
				mg.rating(imp,crw,1)
			else:
				mg.rating(imp,crw)
		elif "SB" in crw:
			if rm.randrange(10) < 8:
				mg.rating(imp,crw)
			else:
				mg.rating(imp,crw,1)
		else:
			if rm.randrange(10) < 7:
				mg.rating(imp, crw)
			else:
				mg.rating(imp,crw,1)
	for n in names:
		mg.check(n)

if __name__ == "__main__":
    main()