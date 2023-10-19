{{ config(materialized='view') }}
-- we use views incase we donot need constant refreshing of data

select 
    -- to create unique key for model
    {{ dbt_utils.surrogate_key(['bikeid','start_station_id', 'end_station_id']) }} as trip_id,
    TIMESTAMP_SECONDS(cast(tripduration / 1000000000 as bigint)) as tripduration,
    TIMESTAMP_SECONDS(cast(starttime / 1000000000 as bigint)) as starttime,
    TIMESTAMP_SECONDS(cast(stoptime / 1000000000 as bigint)) as stoptime,
    start_station_id,
    start_station_name,
    start_station_latitude,
    start_station_longitude,
    end_station_id,
    end_station_name,
    end_station_latitude,
    end_station_longitude,
    bikeid,
    usertype,
    birth_year,
    gender,
    {{ get_age_of_users('birth_year') }} as age_of_users,
    ROUND({{ dbt_utils.haversine_distance('start_station_latitude','start_station_longitude', 'end_station_latitude', 'end_station_longitude') }}, 2) as distance_covered
from {{source('staging', 'Citibikes')}}

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}