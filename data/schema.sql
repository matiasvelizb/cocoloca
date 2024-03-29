CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    guild_id bigint UNIQUE NOT NULL,
    prefix TEXT NOT NULL DEFAULT 'c!',
    turnips bigint[]
); CREATE TABLE IF NOT EXISTS members (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    member_id bigint UNIQUE NOT NULL,
    reputation bigint NOT NULL DEFAULT 0,
    birthday TIMESTAMPTZ,
    switch_name TEXT,
    friend_code TEXT UNIQUE,
    char_name TEXT,
    island_name TEXT,
    hemisphere TEXT,
    nookazon_id bigint
); CREATE TABLE IF NOT EXISTS reps (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY,
    author_id bigint UNIQUE NOT NULL,
    member_id bigint UNIQUE NOT NULL,
    reputation smallint NOT NULL,
    rep_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(author_id, member_id)
);
