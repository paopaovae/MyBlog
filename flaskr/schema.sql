
drop table if exists users;

drop table if exists categories;

drop table if exists topics;

drop table if exists posts;

CREATE TABLE users (
user_id     INTEGER NOT NULL PRIMARY KEY,
user_name   VARCHAR(30) NOT NULL UNIQUE,
user_pass   VARCHAR(255) NOT NULL,
user_email  VARCHAR(255) NOT NULL,
user_date   DATETIME NOT NULL,
user_level  INT8 NOT NULL
);

CREATE TABLE categories (
cat_id INTEGER  NOT NULL PRIMARY KEY,
cat_name VARCHAR(255) NOT NULL UNIQUE,
cat_description VARCHAR(255) NOT NULL
);

CREATE TABLE topics (
topic_id INTEGER NOT NULL PRIMARY KEY,
topic_subject VARCHAR(255) NOT NULL,
topic_date DATETIME NOT NULL,
topic_name VARCHAR(30) NOT NULL,
topic_cat INTEGER NOT NULL REFERENCES categories(cat_id) ON DELETE CASCADE ON UPDATE CASCADE,
topic_by INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE posts (
post_id INTEGER NOT NULL PRIMARY KEY,
post_content TEXT NOT NULL,
post_date       DATETIME NOT NULL,
post_topic      INTEGER NOT NULL REFERENCES topics(topic_id) ON  DELETE CASCADE  ON UPDATE CASCADE,
post_by INTEGER NOT NULL REFERENCES users(user_id) ON DELETE  RESTRICT ON UPDATE CASCADE
);
