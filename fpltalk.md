
```sql
CREATE TABLE gw_combined AS SELECT * FROM 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/gws/merged_gw.csv';
```

```sql
CREATE TABLE fixtures AS SELECT * FROM 'data/fixtures.json';
```


```sql
create table teams as SELECT UNNEST(teams, recursive := true) FROM (from read_json_auto('https://fantasy.premierleague.com/api/bootstrap-static/')) ;
```



```sql
create or replace view players_avg_bonus as (select name, avg(minutes) mins, avg(bonus) bonus from gw_combined group by all) ;
```



```sql
create or replace view topplayers as (from players_avg_bonus where mins >50 order by bonus DESC limit 100) ;
```

```sql
with topclubs as (select distinct ON(team, gw_combined.name) team, gw_combined.name  from gw_combined join topplayers on gw_combined.name = topplayers.name ) select team, count(*) cnt from topclubs group by all order by cnt DESC
```



```sql
create view todays_fixtures as select team_h, team_a from fixtures where event = (select min(event) from fixtures where kickoff_time > now());
```


```sql
create
or replace view team_stats as with topclubs as (select distinct ON(team, gw_combined.name) team, gw_combined.name  from gw_combined join topplayers on gw_combined.name = topplayers.name ), team_cnt as (select team, count(*) cnt from topclubs group by all)
select team_cnt.*, teams.id
from team_cnt
         join teams on teams.name = team_cnt.team;
```



```sql
select *, hcnt - acnt
from (select *, h.cnt hcnt, a.cnt acnt
      from todays_fixtures
               join team_stats h on h.id = team_h
               join team_stats a on a.id = team_a)
order by hcnt - acnt;
```
