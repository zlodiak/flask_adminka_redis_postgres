```
project name: flask_adminka
DB name: flask_adminka
DB admin login: flask_admin
DB admin password: flask_admin
```

table 'users' contains auth data
```
users(email/password):
flask_admin1@ad.ad/flask_admin1
flask_admin2@ad.ad/flask_admin2
flask_admin3@ad.ad/flask_admin3
```

изначально существуют 3 пользователя с определёнными паролями(таблица users). для каждого пользователя в таблице options существует соответствующая запись, в которой хранятся настройки админки.

ниже sql-код для создания таблиц. бекапы этих таблиц есть в текущем каталоге.

```
CREATE TABLE public.users
(
  id integer NOT NULL,
  password_hash text NOT NULL,
  email text NOT NULL,
  active boolean,
  CONSTRAINT id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.users
  OWNER TO flask_admin;
```

```
CREATE TABLE public.options
(
  id integer NOT NULL,
  firstname text,
  lastname text,
  notepad text,
  user_id integer NOT NULL,
  CONSTRAINT options_pkey PRIMARY KEY (id),
  CONSTRAINT user_id FOREIGN KEY (user_id)
      REFERENCES public.users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.options
  OWNER TO flask_admin;

```

используются 2 хранилища данных: redis, postgres. в postgres хранятся все данные, в redis только не критически важные(firstname, lastname, notepad).

номер используемой БД в redis 4.



