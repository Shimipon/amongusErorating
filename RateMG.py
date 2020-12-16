import math
import sqlite3


class RateMG:
	def regist(self, name, im = 1500, cr = 1500):
		conn = sqlite3.connect('PlayerList.db')
		c = conn.cursor()
		c.execute("INSERT INTO Players (name, im, cr) VALUES (?, ?, ?) ", (name, im, cr,))
		conn.commit()
		conn.close()

	def delete(self, name):
		conn = sqlite3.connect('PlayerList.db')
		c = conn.cursor()
		c.execute("DELETE FROM Players WHERE name = ?", (name,))
		conn.commit()
		conn.close()

	def win_CrwImp(self, IMP, CRW):
		ISUM = 0.0
		CSUM = 0.0
		for i in IMP:
			ISUM = ISUM + i[1]
		for i in CRW:
			CSUM = CSUM + i[2]
		divisor = 10.0 ** ((ISUM / len(IMP) - CSUM / len(CRW)) / 400.0) + 1
		return 1.0 / divisor

	def win_ImpCrw(self, IMP, CRW):
		ISUM = 0.0
		CSUM = 0.0
		for i in IMP:
			ISUM = ISUM + i[1]
		for i in CRW:
			CSUM = CSUM + i[2]
		divisor = 10.0 ** ((CSUM / len(CRW) - ISUM / len(IMP)) / 400.0) + 1
		return 1.0 / divisor


	def update(self, IMP, CRW, IWin = 0):
		conn = sqlite3.connect('PlayerList.db')
		c = conn.cursor()
		tIMP = []
		tCRW = []
		ISUM = 0
		CSUM = 0
		for i in IMP:
			c.execute("SELECT * FROM Players WHERE name = ?", (i,))
			tIMP = tIMP + c.fetchall()
		for i in CRW:	
			c.execute("SELECT * FROM Players WHERE name = ?", (i,))
			tCRW = tCRW + c.fetchall()
		for p in tIMP:
			ISUM = ISUM + p[1]
		for p in tCRW:
			CSUM = CSUM + p[2]
		print(tIMP, tCRW)
		rIMP = []
		rCRW = []
		if IWin == 0:
			WIC = self.win_ImpCrw(tIMP, tCRW)
			for p in tIMP:
				nr = p[1] - int(64 * WIC * p[1] / ISUM)
				rIMP = rIMP + [(p[0], nr, p[2])]
			for p in tCRW:
				nr = p[2] + int(192 * WIC *((2 * CSUM / len(tCRW) - p[2]) / CSUM))
				rCRW = rCRW + [(p[0], p[1], nr)]
		else:
			WCI = self.win_CrwImp(tIMP, tCRW)
			for p in tIMP:
				nr = p[1] + int(64 * WCI * ((2 * ISUM / len(tIMP) - p[1]) / ISUM))
				rIMP = rIMP + [(p[0], nr, p[2])]
			for p in tCRW:
				nr = p[2] - int(192 * WCI * p[2] / CSUM)
				rCRW = rCRW + [(p[0], p[1], nr)]
		print(rIMP, rCRW)
		for p in rIMP:
			c.execute("UPDATE Players SET im = ?, cr = ? WHERE name = ?", (p[1], p[2], p[0],))
			conn.commit()
		for p in rCRW:
			c.execute("UPDATE Players SET im = ?, cr = ? WHERE name = ?", (p[1], p[2], p[0],))
			conn.commit()
		conn.close()

	def check(self, NAME):
		conn = sqlite3.connect('PlayerList.db')
		c = conn.cursor()
		c.execute("SELECT * FROM Players WHERE name = ?", (NAME,))
		p = c.fetchall()
		conn.commit()
		conn.close()
		print("Imposter Rate", p[0][1])
		print("Crewmate Rate", p[0][2])
		total = p[0][1] + p[0][2]
		print("Total Rate", total)
		return(p[0][1], p[0][2], p[0][1] + p[0][2])