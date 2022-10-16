select a.id 
from krisha_id as a 
    left join krishaaa as b on a.id = b.id 
where b.id is NULL order by 1;