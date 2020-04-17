create table Employee ( 
    EmpID  int NOT NULL,
    Name varchar(255) NOT NULL,
    PRIMARY KEY (EmpID)
);

insert into Employee (EmpID, Name) values(1, "Joe");
insert into Employee (EmpID, Name) values(2, "Bob");
insert into Employee (EmpID, Name) values(3, "Mary");

alter table Employee
add Age int NULL;

insert into Employee 
    (EmpID, Name, Age)
values(4, "Ann", 24);