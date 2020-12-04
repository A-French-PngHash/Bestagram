DROP DATABASE Bestagram;
CREATE DATABASE Bestagram;
USE Bestagram;

CREATE TABLE UserTable(
    id BIGINT NOT NULL,
    name VARCHAR(30) NOT NULL,
    hash VARCHAR(100) NOT NULL,
    token VARCHAR(30),
    token_registration_date DATE,
    description VARCHAR(1000),
    profile_image_path VARCHAR(30),
    PRIMARY KEY (id)
)
ENGINE=INNODB;

CREATE TABLE LikeTable(
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL
)
ENGINE=INNODB;

CREATE TABLE Post(
    id BIGINT NOT NULL,
    image_path VARCHAR(30) NOT NULL,
    user_id BIGINT NOT NULL,
    post_time DATE NOT NULL,
    description VARCHAR(1000),
    PRIMARY KEY(id)
)
ENGINE=INNODB;

CREATE TABLE Follow(
    user_id BIGINT NOT NULL,
    user_id_followed BIGINT NOT NULL
)
ENGINE=INNODB;

-- Indexes
ALTER TABLE UserTable
ADD UNIQUE ind_name (name);

ALTER TABLE LikeTable
ADD INDEX ind_user_id (user_id);

ALTER TABLE LikeTable
ADD INDEX ind_post_id (post_id);

ALTER TABLE Follow
ADD INDEX ind_user_id (user_id);

ALTER TABLE Follow
ADD INDEX ind_user_id_following (user_id_following);

ALTER TABLE Post
ADD INDEX ind_user_id (user_id);

ALTER TABLE LikeTable
ADD CONSTRAINT fk_LikeTable_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

ALTER TABLE LikeTable
ADD CONSTRAINT fk_LikeTable_post_id_id FOREIGN KEY (post_id) REFERENCES Post(id);

ALTER TABLE Follow
ADD CONSTRAINT fk_Follow_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

ALTER TABLE Follow
ADD CONSTRAINT fk_Follow_user_id_following_id FOREIGN KEY (user_id_following) REFERENCES UserTable(id);

ALTER TABLE Post
ADD CONSTRAINT fk_Post_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);