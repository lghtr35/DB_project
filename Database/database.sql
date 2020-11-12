CREATE TABLE Users(
    personID INT NOT NULL AUTO_INCREMENT,
    Firstname VARCHAR(127) NOT NULL,
    Lastname VARCHAR(127) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (email)
);
CREATE TABLE Posts(
    personID INT NOT NULL,
    post_data VARCHAR(255) NOT NULL,
    name_author VARCHAR(255) NOT NULL,
    pub_date  DATETIME NOT NULL,
    PRIMARY KEY (personID)
);
CREATE TABLE Passes(
    personID INT NOT NULL,
    pass VARCHAR(255) NOT NULL,
    PRIMARY KEY (personID)
);
