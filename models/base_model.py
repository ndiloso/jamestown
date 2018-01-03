import os
from peewee import Model
from playhouse.pool import PooledPostgresqlDatabase
from urllib import parse



parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])




# db_name = os.environ.get("DB_NAME")
# db_host = os.environ.get("DB_HOST")
# db_user = os.environ.get("DB_USER")
# db_password = os.environ.get("DB_PASSWORD")

db_name = url.path[1:]
db_host = url.hostname
db_user = url.username
db_password = url.password
# db_port=url.port

class DBSingelton():
	db = None

	@classmethod
	def getInstance(cls):
		if not cls.db:
			cls.db = PooledPostgresqlDatabase(db_name, **{'user': db_user,
				'host': db_host,
				'password': db_password})


		return cls.db


class BaseModel(Model):
	class Meta:
		database = DBSingelton.getInstance()
	
