from datetime import date
from DBConnection import Database

# Default database location

def create_table():
    create_query = '''
        CREATE TABLE IF NOT EXISTS tb_votes (
            vote_id     INTEGER PRIMARY KEY,
            vote_date   TEXT,
            user_email  TEXT,
            voted_snack TEXT
        );'''
    with Database(Models.DB_FILE) as db:
        db.cursor.execute(create_query)


class Models:
    DB_FILE = "snacks.db"


class Votes(Models):

    def __init__(self, email):
        self.user_email = email

    def register_votes(self, votes):
        """
        Insert votes into VOTES table
        :param votes: list of voted_snack
        """
        query_string = "INSERT INTO tb_votes(vote_date, user_email, voted_snack) VALUES(?,?,?)"
        # Dates saved are in year-mm-dd format
        vote_date = date.today().strftime("%Y-%m-%d")
        with Database(Models.DB_FILE) as db:
            for v in votes:
                db.cursor.execute(query_string, (vote_date, self.user_email, v))

    @staticmethod
    def get_tally(year, month):
        """
        get tally of votes for a specific month
        :param year: integer year eg. 2018
        :param month: integer month eg. 2
        :returns: dictionary for the snacks vote tally {"snack name": 4, ...}
        """
        # Convert the saved dates to month format year-mm
        query_string = '''
            SELECT voted_snack, COUNT(vote_id) as tally
            FROM tb_votes
            WHERE strftime('%Y-%m', vote_date) = :month GROUP BY (voted_snack);
        '''
        vote_month = "{}-{:02d}".format(2018, 2)

        with Database(Models.DB_FILE) as db:
            db.cursor.execute(query_string, {"month": vote_month})
            rows = db.cursor.fetchall()
        return dict(rows)

    def get_allowed_votes(self):
        """
        Get allowed votes for a specific user for the current month
        :returns: int allowed votes left for this user
        """
        max_vote_per_month = 3
        # Month format year-mm
        query_string = '''
            SELECT COUNT(voted_snack) as voted_times
            FROM tb_votes
            WHERE strftime('%Y-%m', vote_date) = :month AND user_email = :email
        '''
        current_month = date.today().strftime("%Y-%m")

        with Database(Models.DB_FILE) as db:
            db.cursor.execute(query_string, {"month": current_month, "email": self.user_email})
            rows = db.cursor.fetchone()

        voted_times = rows[0]
        allowed_votes = max(0, max_vote_per_month - voted_times)
        return allowed_votes
