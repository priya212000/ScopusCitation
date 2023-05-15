create database citations;
use citations;
CREATE TABLE `report` (
  `orcid` varchar(25) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`orcid`)
);
INSERT INTO `report` VALUES ('0000-0001-5054-280X','Ms.Kamalaveni V.'),
('0000-0001-5077-255X','Dr.Latha Parameswaran');


INSERT INTO `report` VALUES ('0000-0001-5054-280X','Ms.Kamalaveni V.'),
('0000-0001-5077-255X','Dr.Latha Parameswaran'),
('0000-0001-5546-4919','Ms.Ramya.U.M.'),
('0000-0001-5846-5343','Ms.Vidhya S'),
('0000-0001-6505-4016','Dr.Thangavelu S.'),
('0000-0001-6591-1655','Ms.Sini Raj .P'),
('0000-0001-6762-3825','Ms.Sathiya. R. R'),
('0000-0001-7243-4850','Dr.Padmavathi.S'),
('0000-0001-7352-6925','Ms.Radhika. G'),
('0000-0001-7560-5846','Mr.Vamsee Krishna Kiran M'),
('0000-0001-7977-2502','Dr.Swapna T.R.'),
('0000-0001-8160-7223','Dr.Senthilkumar T.'),
('0000-0001-8462-1696','Dr.R.Karthi'),
('0000-0001-8834-5641','Dr.Venkataraman D'),
('0000-0001-9215-6122','Dr.P.Prakash'),
('0000-0001-9677-3574','Dr.J.Govindarajan'),
('0000-0002-0344-3005','Dr. C Selvi'),
('0000-0002-0428-6531','Ms.K.P. Jevitha'),
('0000-0002-0502-6467','Ms.Anupa Vijai'),
('0000-0002-1269-2257','Mr.Ritwik.M'),
('0000-0002-1349-2273','Mr.Prashant. R. Nair'),
('0000-0002-2763-9053','Mr.Dayanand V'),
('0000-0002-3499-8062','Ms.Sikha.O.K.'),
('0000-0002-3763-9583','Dr.Bagavathi Sivakumar.P.'),
('0000-0002-4153-010X','Ms.Suchithra M'),
('0000-0002-4301-2330','Ms.G.R.Ramya'),
('0000-0002-4485-0475','Dr.Lalithamani N.'),
('0000-0002-4619-0079','Dr.K.V.Shriram'),
('0000-0002-5501-2338','Dr.Jeyakumar G.'),
('0000-0002-5603-4977.','Ms.Gayathri V'),
('0000-0002-5998-4556','Ms.Subathra P.'),
('0000-0002-6377-640X','Dr.Harini N.'),
('0000-0002-6878-1187','Ms.Archanaa R'),
('0000-0002-6984-2957','Ms.Manjusha R.'),
('0000-0002-7134-8448','Dr. M. Senthilkumar'),
('0000-0002-7628-9483','Ms.Bharathi D'),
('0000-0002-8216-9429','Ms.Prathilothamai M'),
('0000-0002-8239-6904','Dr.Dhanya N M'),
('0000-0002-8246-0523','Dr.Rajathilagam. B'),
('0000-0002-8598-7849','Dr.Priyanka Kumar'),
('0000-0002-8724-5726','Mr.Sumesh.A.K.'),
('0000-0002-9245-9155','Dr.(Col)P.N.Kumar'),
('0000-0002-9335-1568','Dr. Vidhya Balasubramanian'),
('0000-0002-9413-9673','Mr.Sabarish. B. A'),
('0000-0002-9486-5077','Ms.Nalinadevi K.'),
('0000-0002-9619-0931','Ms.Archana Devi.R'),
('0000-0002-9736-0509','Ms.Anisha Radhakrishnan'),
('0000-0002-9979-1644','Mr.Raghesh Krishnan K'),('0000-0003-0094-9497','Ms.Malathi P.'),('0000-0003-0986-1133','Ms.Abirami K'),
('0000-0003-1167-939X','Dr.Anantha Narayanan.V'),('0000-0003-1248-3516','Ms.T. Bagyammal'),('0000-0003-1538-7634','Dr. Gowtham.R.'),
('0000-0003-2000-6824','Mr.Baskar.A'),('0000-0003-2793-2978','Ms.Bindu. K R'),('0000-0003-2983-3201','Mr.Arunkumar. C'),
('0000-0003-3421-654X','Dr.Radhika N.'),('0000-0003-3440-9640','Ms.Sujee. R'),('0000-0003-3762-4311','Dr.C.Shunmuga Velayutham'),
('0000-0003-4332-9407','Ms.Dhanya M Dhanalakshmy'),('0000-0003-4710-6761','Ms.Aarthi. R'),('0000-0003-4728-0225','Dr. Ganesh Neelakanta Iyer'),
('0000-0003-4972-4395','Ms.Shanmuga Priya. S');

drop table report;
select * from report;

select * from report where orcid = '0000-0001-5054-280X';