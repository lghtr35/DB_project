CREATE TABLE Users(
    personID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    F_name VARCHAR(64),
    L_name VARCHAR(64),
    e_mail VARCHAR(64) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    bio VARCHAR(255),
    confirmed BOOLEAN NOT NULL,
    PRIMARY KEY (personID)
);
CREATE TABLE Posts_ids(
    postID INT UNSIGNED NOT NULL AUTO_INCREMENT,
    personID INT UNSIGNED,
    FOREIGN KEY (personID) REFERENCES Users(personID),
    PRIMARY KEY (postID)
);
CREATE TABLE Posts(
    postID INT UNSIGNED,
    payload VARCHAR(511) NOT NULL,
    is_news BOOLEAN NOT NULL,
    publish_date  DATETIME NOT NULL,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (postID)
);
CREATE TABLE Events(
    postID INT UNSIGNED,
    payload VARCHAR(511) NOT NULL,
    publish_date  DATETIME NOT NULL,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (postID)
);
CREATE TABLE Items(
    postID INT UNSIGNED,
    payload VARCHAR(511) NOT NULL,
    price INT NOT NULL,
    publish_date  DATETIME NOT NULL,
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
    publish_date  DATETIME NOT NULL,
    data_type TINYINT NOT NULL,
    FOREIGN KEY (postID) REFERENCES Posts_ids(postID),
    PRIMARY KEY (comment_id)
);