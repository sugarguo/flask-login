CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(64), 
	password_hash VARCHAR(128), 
	email VARCHAR(128), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);

