
#MySQL code for minor bills:
UPDATE billsNEW
SET minorBill = 1
WHERE  (`OfficialTitle` LIKE  '% land%' AND `OfficialTitle` LIKE  '%exchange%') OR
(`OfficialTitle` LIKE  '% land%' AND `OfficialTitle` LIKE  '%transfer%') OR
(`OfficialTitle` LIKE  '% land%' AND `OfficialTitle` LIKE  '%claim%') OR
(`OfficialTitle` LIKE  '%designat%' AND `OfficialTitle` LIKE  '%locat%') OR
(`OfficialTitle` LIKE  '%designat%' AND `OfficialTitle` LIKE  '%building%') OR
OfficialTitle LIKE '%commemora%' OR
OfficialTitle LIKE '%medal%' OR
OfficialTitle LIKE '%coin%' OR
OfficialTitle LIKE '%technical correction%' OR
OfficialTitle LIKE '%convey%' ;

# Update from oldBILLS
#UPDATE billsNEW n, bills b
#SET n.PLawNoFull = b.PLawNum
#WHERE b.id = n.idOLD;


UPDATE billsNEW n, cbp_main.bills b
SET n.Major = b.Major, n.Minor = b.Minor
WHERE b.id = n.idOLD;





#UPDATE URL:
UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/house-bill/',billNum)
WHERE BillType = 'hr';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/house-resolution/',billNum)
WHERE BillType = 'hres';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/house-concurrent-resolution/',billNum)
WHERE BillType = 'hconres';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/house-joint-resolution/',billNum)
WHERE BillType = 'hjres';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/senate-bill/',billNum)
WHERE BillType = 's';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/senate-resolution/',billNum)
WHERE BillType = 'sres';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/senate-concurrent-resolution/',billNum)
WHERE BillType = 'sconres';

UPDATE billsNEW
SET URL = CONCAT('http://beta.congress.gov/bill/',cong,'th-congress/senate-joint-resolution/',billNum)
WHERE BillType = 'sjres';


# Combine Committee Leadership
 
UPDATE billsNEW
SET `LeadRef` = ChRef + RankRef + SubChRef + SubRankRef;

UPDATE billsNEW
SET `LeadRef` = 1
WHERE `LeadRef` = 2;


# Set Chamber Variable (Senate)
UPDATE billsNEW
SET Senate = 1
WHERE BillType = 's' OR BillType = 'sres' OR BillType = 'sconres' OR BillType = 'sjres'; 

UPDATE billsNEW b, members m
SET b.SpParty = m.simpleParty
WHERE b.SpThomasID = m.thomas AND b.cong = m.Cong;


UPDATE billsNEW
SET isBill = 1
WHERE BillType = 's' OR BillType = 'hr';

UPDATE billsNEW
SET Majority = 1
WHERE 
(Senate = 1 AND SpParty = 'D' AND IntrDate < '1981-01-02') OR
(Senate = 1 AND SpParty = 'R' AND IntrDate BETWEEN '1981-01-02' AND '1987-01-01') OR
(Senate = 1 AND SpParty = 'D' AND IntrDate BETWEEN '1987-01-02' AND '1995-01-01')  OR
(Senate = 1 AND SpParty = 'R' AND IntrDate BETWEEN '1995-01-02' AND '2001-01-01')  OR  
(Senate = 1 AND SpParty = 'D' AND IntrDate BETWEEN '2001-01-02' AND '2001-01-19')     OR
(Senate = 1 AND SpParty = 'R' AND IntrDate BETWEEN '2001-01-20' AND '2001-06-05')  OR
(Senate = 1 AND SpParty = 'D' AND IntrDate BETWEEN '2001-06-06' AND '2003-01-01') OR
(Senate = 1 AND SpParty = 'R' AND IntrDate BETWEEN '2003-01-02' AND '2007-01-01') OR
(Senate = 1 AND SpParty = 'D' AND IntrDate BETWEEN '2007-01-02' AND '2015-01-01') OR
(Senate = 0 AND SpParty = 'D' AND IntrDate <'1995-01-02') OR 
(Senate = 0 AND SpParty = 'R' AND IntrDate BETWEEN '1995-01-02' AND '2007-01-01') OR 
(Senate = 0 AND SpParty = 'D' AND IntrDate BETWEEN '2007-01-02' AND '2011-01-01') OR  
(Senate = 0 AND SpParty = 'R' AND IntrDate BETWEEN '2011-01-02' AND '2015-01-01');    



UPDATE billsNEW n, cbp_main.bills_companion c
SET n.compLaw = c.lawIDNew
WHERE LOWER(c.BillType) = n.BillType
AND c.cong = n.Cong
AND c.BillNum = n.BillNum;


# Reset actionID to be sequential
ALTER TABLE `actions` DROP `actionID`;
ALTER TABLE `actions` AUTO_INCREMENT = 1;
ALTER TABLE `actions` ADD `actionID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY;

# Remove quotes from bill titles
UPDATE billsNEW SET OfficialTitle = REPLACE(OfficialTitle, '`', ''); 
UPDATE billsNEW SET OfficialTitle = REPLACE(OfficialTitle, '"', ''); 
UPDATE billsNEW SET OfficialTitle = REPLACE(OfficialTitle, '\'', '');

UPDATE billsNEW SET ShortTitle = REPLACE(ShortTitle, '`', ''); 
UPDATE billsNEW SET ShortTitle = REPLACE(ShortTitle, '"', ''); 
UPDATE billsNEW SET ShortTitle = REPLACE(ShortTitle, '\'', '');


########## MEMBERS UPDATE ############
#DW UPDATE:
#UPDATE members m, DWNom d
#SET m.DW1 = d.DW1
#WHERE m.cong = d.Cong AND
#m.ICPSR = d.ICPSR 
#and m.DW1 IS NULL

#UPDATE members
#SET simpleParty = 'D'
#WHERE party = 'Democrat'
#OR party = 'Democrat Farmer Labor'
#OR party = 'Democrat-Liberal'
#OR party = 'Democrat/Independent'
#OR party = 'Ind. Democrat'
#OR party = 'Democrat/Republican';

#UPDATE members
#SET simpleParty = 'R'
#WHERE party = 'Republican'
#OR party = 'Republican-Conservative'
#OR party = 'Conservative'
#OR party = 'Democrat-turned-Republican'
#OR party = 'Independent/Republican';

#UPDATE members
#SET simpleParty = 'I'
#WHERE party = 'Independent'
#OR party = 'New Progressive'
#OR party = 'Popular Democrat'
#OR party = 'AL';