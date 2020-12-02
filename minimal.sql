create table if not exists user(
  id integer primary key,
  name text unique not null,
  password text not null
);

create table if not exists agenda(
  id integer primary key,
  user_id integer references user(id),
  created timestamp not null default current_timestamp,
  title text not null,
  body text not null
);

insert or ignore into user(id, name, password) select 1, 'xxx', 'yyy';
insert or ignore into agenda(id, user_id, title, body) select 1, 1, 'aaa', 'bbb';
