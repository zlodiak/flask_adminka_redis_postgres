```
project name: flask_adminka
DB name: flask_adminka
DB admin login: flask_admin
DB admin password: flask_admin
```

table 'users' contains auth data
```
users(email/password):
q/qq
w/ww
```


ниже sql-код для создания таблиц. бекапы этих таблиц есть в текущем каталоге.

```
CREATE TABLE public.options
(
  id integer NOT NULL DEFAULT nextval('increment'::regclass),
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

```
CREATE TABLE public.users
(
  id integer NOT NULL DEFAULT nextval('increment'::regclass),
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

используются 2 хранилища данных: redis, postgres. в postgres хранятся все данные, redis служит кешем для: firstname, lastname, notepad.

номер используемой БД в redis 4.



