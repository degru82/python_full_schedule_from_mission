create table tb_linkonroute (
    ROUT_LINK_ID varchar(10) ,
    LINK_SEQ decimal(5,0)
);

create table tb_stoppoint (
    STOPPOINT_ID varchar(10),
    ROUT_LINK_ID varchar(10),
    JRNY_PATTRN_ID varchar(10)

);

create table tb_jrnypattrn (
    JRNY_PATTRN_ID varchar(10)
);


insert into tb_linkonroute
(ROUT_LINK_ID, LINK_SEQ)
values
('RL_1000001', 1);

insert into tb_linkonroute
(ROUT_LINK_ID, LINK_SEQ)
values
('RL_1000003', 2);

insert into tb_linkonroute
(ROUT_LINK_ID, LINK_SEQ)
values
('RL_1000005', 3);

insert into tb_linkonroute
(ROUT_LINK_ID, LINK_SEQ)
values
('RL_1000007', 4);

insert into tb_linkonroute
(ROUT_LINK_ID, LINK_SEQ)
values
('RL_1000009', 5);

insert into tb_linkonroute
(ROUT_LINK_ID, LINK_SEQ)
values
('RL_1000011', 6);


insert into tb_jrnypattrn
(JRNY_PATTRN_ID)
values (
    'JP_1000001'
);



insert into tb_stoppoint (STOPPOINT_ID, ROUT_LINK_ID, JRNY_PATTRN_ID) 
values ('SP_1000001', 'RL_1000001', 'JP_1000001');

insert into tb_stoppoint (STOPPOINT_ID, ROUT_LINK_ID, JRNY_PATTRN_ID) 
values ('SP_1000002', 'RL_1000003', 'JP_1000001');

insert into tb_stoppoint (STOPPOINT_ID, ROUT_LINK_ID, JRNY_PATTRN_ID) 
values ('SP_1000003', 'RL_1000007', 'JP_1000001');

insert into tb_stoppoint (STOPPOINT_ID, ROUT_LINK_ID, JRNY_PATTRN_ID) 
values ('SP_1000004', 'RL_1000011', 'JP_1000001');




create table tb_servicerequest (
    SVC_REQ_ID varchar(10),
    PICKUP_STOPPOINT_ID varchar(10),
    MSSN_ID_FOR_PICKUP varchar(10),
    DROPOFF_STOPPOINT_ID varchar(10),
    MSSN_ID_FOR_DROPOFF varchar(10),
    NUM_OF_PASSNGR decimal(5,0)
);

create table tb_mission (
    MSSN_ID varchar(10),
    STOPPOINT_ID varchar(10),
    VISIT_SEQ decimal(5,0),
    PASSNGR_CHANGE decimal(5,0)
);

