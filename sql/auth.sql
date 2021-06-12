
CREATE TABLE Users
(
    id                      text            PRIMARY KEY,
    name                    text,
    username                text            UNIQUE,
    email                   text            UNIQUE,
    photo                   text,
    create_date             timestamptz,
    status                  smallint
);

CREATE TABLE UserHandle
(
    user_id                 text             REFERENCES Users(id),
    handle_provider         text,
    handle_user_id          text,
    handle_name             text,
    handle_connection       text
);
