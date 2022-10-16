--sorting ID via Left Exclusive Join
select a.id 
from krisha_id as a 
    left join krishaaa as b on a.id = b.id 
where b.id is NULL order by 1;


--sorting most expensive apartment
--Цена - price
--Город - city
select Цена
from krisha_id
group by Город
