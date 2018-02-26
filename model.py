from datetime import date
from dbConnection import Database

db_file = "snacks.db"

def create_table():
	create_query = '''
		CREATE TABLE IF NOT EXISTS tb_votes (
			vote_id		INTEGER PRIMARY KEY,
			vote_date	TEXT,
			user_email	TEXT,
			voted_snack	TEXT
		);'''
	with Database(db_file) as db:
		db.cursor.execute(create_query)

def register_votes(votes, email):
    """
    Insert votes into VOTES table
    :param votes: list of voted_snack
    :param email: string email
    """
    query_string = "INSERT INTO tb_votes(vote_date, user_email, voted_snack) VALUES(?,?,?)"
    # dates saved are in year-mm-dd format
	vote_date = date.today().strftime("%Y-%m-%d")
    with Database(db_file) as db:
	    for v in votes:
    		db.cursor.execute(query_string, (vote_date, email, v))

def get_tally(year, month):
	"""
	get tally of votes for a specific month
	:param year: integer year eg. 2018
	:param month: integer month eg. 02
	:returns:
	"""
	# convert the saved dates to month format year-mm
	query_string = '''
		SELECT voted_snack, COUNT(voted_snack) as tally
		FROM tb_votes
		WHERE strftime('%Y-%m', vote_date) = :month GROUP BY (voted_snack);
	'''
	vote_month = year + "-" + month
	with Database(db_file) as db:
		db.cursor.execute(query_string, {"month":vote_month})
		rows = db.cursor.fetchall()
	return rows

def get_allowed_votes(email):
	"""
	get allowed votes for a specific user for the current month
	:param email: string email
	:returns:
	"""
	# month format year-mm
	query_string = '''
		SELECT COUNT(voted_snack) as voted_times
		FROM tb_votes
		WHERE strftime('%Y-%m', vote_date) = :month AND user_email = :email
	'''
	current_month = date.today().strftime("%Y-%m")

	with Database(db_file) as db:
		db.cursor.execute(query_string, {"month": current_month, "email": email})
		rows = db.cursor.fetchall()

	voted_times = rows[0]
	allowed_votes = max(0, 3 - voted_times)
	return allowed_votes
