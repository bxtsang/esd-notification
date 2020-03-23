drop schema if exists petrol;
create schema petrol;
use petrol;

drop table if exists petrol;
create table `petrol` (
    `name` varchar (20) not null,
    `rating` int,
    `storage` double default 0.0
);

insert into petrol (name, rating)
values 
    ("Basic X1", 92),
    ("Cool X2", 95),
    ("Fantastic X3", 92),
    ("Diesel", null)
;
