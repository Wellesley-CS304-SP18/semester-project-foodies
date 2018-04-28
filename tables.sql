/*
CS304 Final Project
Created by: Megan Shum, Mina Hattori, and Maxine Hood
*/

drop table if exists comments;
drop table if exists likes;
drop table if exists profile;
drop table if exists posts;
drop table if exists followers;
drop table if exists user;

create table user(
	username varchar(50) not null primary key,
	password varchar(50) not null,
	name varchar(50) not null,
	email varchar(50) not null
)
ENGINE = InnoDB;

create table profile(
	username varchar(50) not null primary key,
	INDEX(username)
	foreign key (username) references user(username),
	description varchar(150)
)
ENGINE = InnoDB;

create table followers(
	follower varchar(50) not null,
	following varchar(50) not null,
	primary key (follower, following),
	INDEX(follower),
	INDEX(following),
	foreign key (follower) references user(username) on delete cascade,
	foreign key (following) references user(username) on delete cascade
)
ENGINE = InnoDB;

create table posts(
	post_id integer unsigned auto_increment primary key,
	username varchar(50) not null,
	description varchar(100),
	location varchar(50),
	pic longblob,
	time_stamp datetime not null,
	INDEX(username),
	foreign key (username) references user(username) on delete cascade
)
ENGINE = InnoDB;

create table likes(
	username varchar(50) not null,
	post_id integer unsigned auto_increment,
	primary key (username, post_id),
	INDEX(username),
	INDEX(post_id),
	foreign key (username) references user(username) on delete cascade,
	foreign key (post_id) references posts(post_id) on delete cascade
)
ENGINE = InnoDB;

create table comments(
	username varchar(50) not null,
	post_id integer unsigned auto_increment,
	comment varchar(300) not null,
	time_stamp datetime not null,
	primary key (username, post_id),
	INDEX(username),
	INDEX(post_id),
	foreign key (username) references user(username) on delete cascade,
	foreign key (post_id) references posts(post_id) on delete cascade
)
ENGINE = InnoDB;
