-- this macro gets the age of bikes as of 2023
{% macro get_age_of_users(birth_year) %}
    2023 - CAST({{ birth_year }} AS integer)
{% endmacro %}

