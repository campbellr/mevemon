CREATE TABLE invTypes (
  typeID smallint(6) NOT NULL,
  groupID smallint(6) default NULL,
  typeName varchar(100) default NULL,
  description varchar(3000) default NULL,
  graphicID smallint(6) default NULL,
  radius double default NULL,
  mass double default NULL,
  volume double default NULL,
  capacity double default NULL,
  portionSize int(11) default NULL,
  raceID tinyint(3) default NULL,
  basePrice double default NULL,
  published tinyint(1) default NULL,
  marketGroupID smallint(6) default NULL,
  chanceOfDuplicating double default NULL
);
