select
    cast(trim(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p>.+</p>'), '<p>|</p>', '')) as NUMBER) as p0
    ,trim(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<h1>.+</h1>'), '<h1>|</h1>', '')) as h1
    ,trim(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<p class="title">|</p>', '')) as title
    ,trim(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<p class="author">|</p>', '')) as author
    ,cast(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="price">.+</p>'), '<p class="price">|</p>|₽', '') as NUMBER) as price_rubles
from data