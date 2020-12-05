# Database Documentation
This document provide a full documentation of the database used in the Bestagram project back end side.

## Type
The database is a MySQL database. All the tables uses the InnoDB motor.

## Naming
Tables names must follow the *CamelCase* convention. 
Indexes must follow the following syntax : *ind_column_name*.
** Example :**

    ALTER TABLE Post  
    ADD INDEX ind_user_id (user_id);

Foreign Keys must follow the following syntax : *fk_table_name_column_name_reference_column_name*
**Example :** 
  

    ALTER TABLE Post  
    ADD CONSTRAINT fk_Post_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

## Construction
If you want to construct the database on your side, first install the *MySQL server* on your computer. Then you can find all the SQL instructions needed in *database.sql* .

## UserTable
This table stores all the **user profile data**. It is named like this because *user* is a key in SQL making it impossible for the table to just be named *User*.

| Field              | Type          | Null | Key | Default | Extra |
| --------------------|---------------|------|-----|---------|-------|
| id                 | bigint        | NO   | PRI | NULL    |       |
| name               | varchar(30)   | NO   | UNI | NULL    |       |
| hash               | varchar(100)  | NO   |     | NULL    |       |
| token                   | varchar(30)   | YES  |     | NULL    |       |
| token_registration_date | date          | YES  |     | NULL    |       |
| description        | varchar(1000) | YES  |     | NULL    |       |
| profile_image_path | varchar(30)   | YES  |     | NULL    |       |
### Id
The id component uniquely identify each user. It is used throughout the other tables to identify elements from a user.
This component cannot be changed by the user who has no access - nor read or write - to it.
### Name
The username chosen by the user. This element is accessible by all user of the app as it is what is shown on the profile of someone. Only the user has a write access to it. It is unique as different people can't have the same name.
### Hash
The hash generated with the user password and username. For more information on how it is generated see *API Documentation.md*.
### Token
When the user send the correct hash as login information, a token is generated (if there is not already one and if it hasn't expired yet) and then sent back to the user. This token is then used as a key for most of the API request. For more information see *API Documentation.md*.
### Token_registration_date
This is the date when the token was generated. To provide more security, tokens are invalidated after a certain time so the user has to send login information again to get the new token.
### Description
The profile description set by the user on his profile. Only the user has a write access to it.
### Profile_image_path
Store a path that link to an image used as a profile image. The user has no direct write access to the path but can change the image by uploading a new one. For more information see *API Documentation.md*.

## Post
Store a post and hit attributes.
| Field       | Type          | Null | Key | Default | Extra |
|-------------|---------------|------|-----|---------|-------|
| id          | bigint        | NO   | PRI | NULL    |       |
| image_path  | varchar(30)   | NO   |     | NULL    |       |
| user_id     | bigint        | NO   | MUL | NULL    |       |
| post_time   | date          | NO   |     | NULL    |       |
| description | varchar(1000) | YES  |     | NULL    |       |
### Id
Is the primary key of this table. Used to uniquely identified a given post in the database.
### Image_path
Is the path leading to the image composing the post itself. The image was chosen by the user and then uploaded.
### User_id
Is the id of the user who created the post. Linked with foreign key to the id component of the user table.
### Post_time
The UTC time when the post was created.
### Description
The description given by the user of the post.

## LikeTable
This table stores all the like given by one user to another. It is named like this because *Like* is a keyword in SQL.
| Field   | Type   | Null | Key | Default | Extra |
|---------|--------|------|-----|---------|-------|
| user_id | bigint | NO   | MUL | NULL    |       |
| post_id | bigint | NO   | MUL | NULL    |       |

### User_id
Is associated with a foreign key with the id field of the User table. Represent the id of the person who liked the given post. It is not unique as a person can like different posts.
### Post_id
Is associated with a foreign key with the id field of the Post table. Represent the id of the post liked by the person. It is not unique as a post can be liked by different persons.

## Follow
This table sores all the following between users.
| Field             | Type   | Null | Key | Default | Extra |
|-------------------|--------|------|-----|---------|-------|
| user_id           | bigint | NO   | MUL | NULL    |       |
| user_id_followed | bigint | NO   | MUL | NULL    |       |
### User_id
This is the id of the user following the other one. Linked with a foreign key to the id field of the user table.
### User_id_followed
This is the id of the user being followed by the other one. Linked with a foreign key to the id field of the user table.