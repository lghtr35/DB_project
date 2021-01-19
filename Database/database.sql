CREATE TABLE Users(
    personID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    F_name VARCHAR(64),
    L_name VARCHAR(64),
    e_mail VARCHAR(64) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    bio VARCHAR(255),
    PRIMARY KEY (personID)
);
CREATE TABLE Friends_of_user(
    personID INT UNSIGNED NOT NULL,
    FriendID INT UNSIGNED NOT NULL,
    FriendshipID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    accepted BOOLEAN NOT NULL,
    FOREIGN KEY (personID) REFERENCES Users(personID),
    PRIMARY KEY (FriendshipID)
);
CREATE TABLE Posts_ids(
    postID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    personID INT UNSIGNED,
    iem_type INT UNSIGNED NOT NULL,
    FOREIGN KEY (personID) REFERENCES Users(personID),
    PRIMARY KEY (postID)
);
CREATE TABLE Posts(
    postID INT UNSIGNED,
    payload VARCHAR(511) NOT NULL,
    is_news BOOLEAN NOT NULL,
    publish_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (postID)
);
CREATE TABLE Events(
    postID INT UNSIGNED,
    payload VARCHAR(511) NOT NULL,
    publish_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (postID)
);
CREATE TABLE Items(
    postID INT UNSIGNED,
    payload VARCHAR(511) NOT NULL,
    price INT NOT NULL,
    publish_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (postID)
);
CREATE TABLE Passes(
    personID INT UNSIGNED ,
    hash_pass VARCHAR(255) NOT NULL,
    FOREIGN KEY (personID) REFERENCES Users(personID),
    PRIMARY KEY (personID)
);
CREATE TABLE Attendee_list(
    personID INT UNSIGNED ,
    postID INT UNSIGNED ,
    FOREIGN KEY (personID) REFERENCES Users(personID),
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (postID)
);
CREATE TABLE Comments_list(
    postID INT UNSIGNED,
    comment_id INT UNSIGNED NOT NULL,
    payload VARCHAR(511) NOT NULL,
    publish_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_type TINYINT NOT NULL,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (comment_id)
);
