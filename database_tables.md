# MetaMystic Database Tables

## Table of Contents

- [account_emailaddress](#account_emailaddress)
- [account_emailconfirmation](#account_emailconfirmation)
- [admin](#admin)
- [astrology_blogpost](#astrology_blogpost)
- [astrology_booking](#astrology_booking)
- [astrology_cartitem](#astrology_cartitem)
- [astrology_consultationreport](#astrology_consultationreport)
- [astrology_contact](#astrology_contact)
- [astrology_order](#astrology_order)
- [astrology_orderitem](#astrology_orderitem)
- [astrology_profile](#astrology_profile)
- [astrology_service](#astrology_service)
- [astrology_userreading](#astrology_userreading)
- [astrology_whatsappconfig](#astrology_whatsappconfig)
- [auth_group](#auth_group)
- [auth_group_permissions](#auth_group_permissions)
- [auth_permission](#auth_permission)
- [auth_user](#auth_user)
- [auth_user_groups](#auth_user_groups)
- [auth_user_user_permissions](#auth_user_user_permissions)
- [blog_post](#blog_post)
- [booking](#booking)
- [cart_item](#cart_item)
- [contact](#contact)
- [django_admin_log](#django_admin_log)
- [django_content_type](#django_content_type)
- [django_migrations](#django_migrations)
- [django_session](#django_session)
- [django_site](#django_site)
- [order](#order)
- [order_item](#order_item)
- [service](#service)
- [socialaccount_socialaccount](#socialaccount_socialaccount)
- [socialaccount_socialapp](#socialaccount_socialapp)
- [socialaccount_socialapp_sites](#socialaccount_socialapp_sites)
- [socialaccount_socialtoken](#socialaccount_socialtoken)

## account_emailaddress

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| email | character varying | 254 | - | NO |
| verified | boolean | - | - | NO |
| primary | boolean | - | - | NO |
| user_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`

### Indexes

- INDEX `account_emailaddress_email_03be32b2` (email)
- INDEX `account_emailaddress_email_03be32b2_like` (email)
- UNIQUE INDEX `account_emailaddress_pkey` (id)
- INDEX `account_emailaddress_user_id_2c513194` (user_id)
- UNIQUE INDEX `account_emailaddress_user_id_email_987c8728_uniq` (email, user_id)
- UNIQUE INDEX `unique_primary_email` (user_id, primary)
- UNIQUE INDEX `unique_verified_email` (email)

---

## account_emailconfirmation

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| created | timestamp with time zone | - | - | NO |
| sent | timestamp with time zone | - | - | YES |
| key | character varying | 64 | - | NO |
| email_address_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `email_address_id` → `account_emailaddress.id`

### Indexes

- INDEX `account_emailconfirmation_email_address_id_5b7f8c58` (email_address_id)
- INDEX `account_emailconfirmation_key_f43612bd_like` (key)
- UNIQUE INDEX `account_emailconfirmation_key_key` (key)
- UNIQUE INDEX `account_emailconfirmation_pkey` (id)

---

## admin

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('admin_id_seq'::regclass) | NO |
| username | character varying | 64 | - | NO |
| email | character varying | 120 | - | NO |
| password_hash | character varying | 256 | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `admin_email_key` (email)
- UNIQUE INDEX `admin_pkey` (id)
- UNIQUE INDEX `admin_username_key` (username)

---

## astrology_blogpost

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| title | character varying | 120 | - | NO |
| slug | character varying | 120 | - | NO |
| content | text | - | - | NO |
| summary | character varying | 200 | - | NO |
| image | character varying | 100 | - | YES |
| published | boolean | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| updated_at | timestamp with time zone | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `astrology_blogpost_pkey` (id)
- INDEX `astrology_blogpost_slug_f1ed1819_like` (slug)
- UNIQUE INDEX `astrology_blogpost_slug_key` (slug)

---

## astrology_booking

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| customer_name | character varying | 100 | - | NO |
| customer_email | character varying | 254 | - | NO |
| customer_phone | character varying | 20 | - | NO |
| booking_date | date | - | - | NO |
| booking_time | time without time zone | - | - | NO |
| notes | text | - | - | NO |
| status | character varying | 20 | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| user_id | integer | - | - | YES |
| service_id | bigint | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`
- `service_id` → `astrology_service.id`

### Indexes

- UNIQUE INDEX `astrology_booking_pkey` (id)
- INDEX `astrology_booking_service_id_4f019502` (service_id)
- INDEX `astrology_booking_user_id_2efc7ac5` (user_id)

---

## astrology_cartitem

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| session_id | character varying | 64 | - | NO |
| quantity | integer | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| service_id | bigint | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `service_id` → `astrology_service.id`

### Indexes

- UNIQUE INDEX `astrology_cartitem_pkey` (id)
- INDEX `astrology_cartitem_service_id_9046895b` (service_id)

---

## astrology_consultationreport

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| title | character varying | 100 | - | NO |
| description | text | - | - | YES |
| report_file | character varying | 100 | - | NO |
| consultation_date | date | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| updated_at | timestamp with time zone | - | - | NO |
| user_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`

### Indexes

- UNIQUE INDEX `astrology_consultationreport_pkey` (id)
- INDEX `astrology_consultationreport_user_id_76a439ee` (user_id)

---

## astrology_contact

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| name | character varying | 100 | - | NO |
| email | character varying | 254 | - | NO |
| subject | character varying | 200 | - | NO |
| message | text | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| is_read | boolean | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `astrology_contact_pkey` (id)

---

## astrology_order

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| order_number | character varying | 20 | - | NO |
| customer_name | character varying | 100 | - | NO |
| customer_email | character varying | 254 | - | NO |
| customer_phone | character varying | 20 | - | NO |
| total_amount | numeric | - | - | NO |
| status | character varying | 20 | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| user_id | integer | - | - | YES |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`

### Indexes

- INDEX `astrology_order_order_number_a7df6222_like` (order_number)
- UNIQUE INDEX `astrology_order_order_number_key` (order_number)
- UNIQUE INDEX `astrology_order_pkey` (id)
- INDEX `astrology_order_user_id_d91400cc` (user_id)

---

## astrology_orderitem

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| service_name | character varying | 100 | - | NO |
| price | numeric | - | - | NO |
| quantity | integer | - | - | NO |
| order_id | bigint | - | - | NO |
| service_id | bigint | - | - | YES |

### Primary Key

- id

### Foreign Keys

- `order_id` → `astrology_order.id`
- `service_id` → `astrology_service.id`

### Indexes

- INDEX `astrology_orderitem_order_id_6cf060f6` (order_id)
- UNIQUE INDEX `astrology_orderitem_pkey` (id)
- INDEX `astrology_orderitem_service_id_319240c5` (service_id)

---

## astrology_profile

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| phone_number | character varying | 128 | - | YES |
| birth_date | date | - | - | YES |
| birth_time | time without time zone | - | - | YES |
| birth_place | character varying | 100 | - | YES |
| bio | text | - | - | YES |
| profile_image | character varying | 100 | - | YES |
| is_phone_verified | boolean | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| updated_at | timestamp with time zone | - | - | NO |
| user_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`

### Indexes

- UNIQUE INDEX `astrology_profile_pkey` (id)
- UNIQUE INDEX `astrology_profile_user_id_key` (user_id)

---

## astrology_service

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| name | character varying | 100 | - | NO |
| slug | character varying | 100 | - | NO |
| description | text | - | - | NO |
| short_description | character varying | 200 | - | NO |
| price | numeric | - | - | NO |
| duration | integer | - | - | NO |
| image | character varying | 100 | - | YES |
| is_available | boolean | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `astrology_service_pkey` (id)
- INDEX `astrology_service_slug_56e239b4_like` (slug)
- UNIQUE INDEX `astrology_service_slug_key` (slug)

---

## astrology_userreading

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| title | character varying | 100 | - | NO |
| content | text | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| is_public | boolean | - | - | NO |
| user_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`

### Indexes

- UNIQUE INDEX `astrology_userreading_pkey` (id)
- INDEX `astrology_userreading_user_id_9ad4e604` (user_id)

---

## astrology_whatsappconfig

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| phone_number | character varying | 128 | - | NO |
| default_message | character varying | 255 | - | NO |
| display_name | character varying | 100 | - | NO |
| is_active | boolean | - | - | NO |
| created_at | timestamp with time zone | - | - | NO |
| updated_at | timestamp with time zone | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `astrology_whatsappconfig_pkey` (id)

---

## auth_group

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| name | character varying | 150 | - | NO |

### Primary Key

- id

### Indexes

- INDEX `auth_group_name_a6ea08ec_like` (name)
- UNIQUE INDEX `auth_group_name_key` (name)
- UNIQUE INDEX `auth_group_pkey` (id)

---

## auth_group_permissions

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| group_id | integer | - | - | NO |
| permission_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `group_id` → `auth_group.id`
- `permission_id` → `auth_permission.id`

### Indexes

- INDEX `auth_group_permissions_group_id_b120cbf9` (group_id)
- UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (group_id, permission_id)
- INDEX `auth_group_permissions_permission_id_84c5c92e` (permission_id)
- UNIQUE INDEX `auth_group_permissions_pkey` (id)

---

## auth_permission

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| name | character varying | 255 | - | NO |
| content_type_id | integer | - | - | NO |
| codename | character varying | 100 | - | NO |

### Primary Key

- id

### Foreign Keys

- `content_type_id` → `django_content_type.id`

### Indexes

- INDEX `auth_permission_content_type_id_2f476e4b` (content_type_id)
- UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq` (content_type_id, codename)
- UNIQUE INDEX `auth_permission_pkey` (id)

---

## auth_user

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| password | character varying | 128 | - | NO |
| last_login | timestamp with time zone | - | - | YES |
| is_superuser | boolean | - | - | NO |
| username | character varying | 150 | - | NO |
| first_name | character varying | 150 | - | NO |
| last_name | character varying | 150 | - | NO |
| email | character varying | 254 | - | NO |
| is_staff | boolean | - | - | NO |
| is_active | boolean | - | - | NO |
| date_joined | timestamp with time zone | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `auth_user_pkey` (id)
- INDEX `auth_user_username_6821ab7c_like` (username)
- UNIQUE INDEX `auth_user_username_key` (username)

---

## auth_user_groups

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| user_id | integer | - | - | NO |
| group_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`
- `group_id` → `auth_group.id`

### Indexes

- INDEX `auth_user_groups_group_id_97559544` (group_id)
- UNIQUE INDEX `auth_user_groups_pkey` (id)
- INDEX `auth_user_groups_user_id_6a12ed8b` (user_id)
- UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq` (user_id, group_id)

---

## auth_user_user_permissions

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| user_id | integer | - | - | NO |
| permission_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`
- `permission_id` → `auth_permission.id`

### Indexes

- INDEX `auth_user_user_permissions_permission_id_1fbb5f2c` (permission_id)
- UNIQUE INDEX `auth_user_user_permissions_pkey` (id)
- INDEX `auth_user_user_permissions_user_id_a95ead1b` (user_id)
- UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (user_id, permission_id)

---

## blog_post

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('blog_post_id_seq'::regclass) | NO |
| title | character varying | 120 | - | NO |
| slug | character varying | 120 | - | NO |
| content | text | - | - | NO |
| summary | character varying | 200 | - | YES |
| image_url | character varying | 256 | - | YES |
| published | boolean | - | - | YES |
| created_at | timestamp without time zone | - | - | YES |
| updated_at | timestamp without time zone | - | - | YES |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `blog_post_pkey` (id)
- UNIQUE INDEX `blog_post_slug_key` (slug)

---

## booking

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('booking_id_seq'::regclass) | NO |
| service_id | integer | - | - | NO |
| customer_name | character varying | 100 | - | NO |
| customer_email | character varying | 120 | - | NO |
| customer_phone | character varying | 20 | - | YES |
| booking_date | date | - | - | NO |
| booking_time | time without time zone | - | - | NO |
| notes | text | - | - | YES |
| status | character varying | 20 | - | YES |
| created_at | timestamp without time zone | - | - | YES |

### Primary Key

- id

### Foreign Keys

- `service_id` → `service.id`

### Indexes

- UNIQUE INDEX `booking_pkey` (id)

---

## cart_item

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('cart_item_id_seq'::regclass) | NO |
| session_id | character varying | 64 | - | NO |
| service_id | integer | - | - | NO |
| quantity | integer | - | - | YES |
| created_at | timestamp without time zone | - | - | YES |

### Primary Key

- id

### Foreign Keys

- `service_id` → `service.id`

### Indexes

- UNIQUE INDEX `cart_item_pkey` (id)

---

## contact

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('contact_id_seq'::regclass) | NO |
| name | character varying | 100 | - | NO |
| email | character varying | 120 | - | NO |
| subject | character varying | 200 | - | YES |
| message | text | - | - | NO |
| created_at | timestamp without time zone | - | - | YES |
| is_read | boolean | - | - | YES |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `contact_pkey` (id)

---

## django_admin_log

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| action_time | timestamp with time zone | - | - | NO |
| object_id | text | - | - | YES |
| object_repr | character varying | 200 | - | NO |
| action_flag | smallint | - | - | NO |
| change_message | text | - | - | NO |
| content_type_id | integer | - | - | YES |
| user_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `content_type_id` → `django_content_type.id`
- `user_id` → `auth_user.id`

### Indexes

- INDEX `django_admin_log_content_type_id_c4bce8eb` (content_type_id)
- UNIQUE INDEX `django_admin_log_pkey` (id)
- INDEX `django_admin_log_user_id_c564eba6` (user_id)

---

## django_content_type

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| app_label | character varying | 100 | - | NO |
| model | character varying | 100 | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq` (app_label, model)
- UNIQUE INDEX `django_content_type_pkey` (id)

---

## django_migrations

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| app | character varying | 255 | - | NO |
| name | character varying | 255 | - | NO |
| applied | timestamp with time zone | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `django_migrations_pkey` (id)

---

## django_session

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| session_key | character varying | 40 | - | NO |
| session_data | text | - | - | NO |
| expire_date | timestamp with time zone | - | - | NO |

### Primary Key

- session_key

### Indexes

- INDEX `django_session_expire_date_a5c62663` (expire_date)
- UNIQUE INDEX `django_session_pkey` (session_key)
- INDEX `django_session_session_key_c0390e0f_like` (session_key)

---

## django_site

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| domain | character varying | 100 | - | NO |
| name | character varying | 50 | - | NO |

### Primary Key

- id

### Indexes

- INDEX `django_site_domain_a2e37b91_like` (domain)
- UNIQUE INDEX `django_site_domain_a2e37b91_uniq` (domain)
- UNIQUE INDEX `django_site_pkey` (id)

---

## order

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('order_id_seq'::regclass) | NO |
| order_number | character varying | 20 | - | NO |
| customer_name | character varying | 100 | - | NO |
| customer_email | character varying | 120 | - | NO |
| customer_phone | character varying | 20 | - | YES |
| total_amount | double precision | - | - | NO |
| status | character varying | 20 | - | YES |
| created_at | timestamp without time zone | - | - | YES |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `order_order_number_key` (order_number)
- UNIQUE INDEX `order_pkey` (id)

---

## order_item

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('order_item_id_seq'::regclass) | NO |
| order_id | integer | - | - | NO |
| service_id | integer | - | - | NO |
| service_name | character varying | 100 | - | NO |
| price | double precision | - | - | NO |
| quantity | integer | - | - | YES |

### Primary Key

- id

### Foreign Keys

- `order_id` → `order.id`
- `service_id` → `service.id`

### Indexes

- UNIQUE INDEX `order_item_pkey` (id)

---

## service

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | nextval('service_id_seq'::regclass) | NO |
| name | character varying | 100 | - | NO |
| slug | character varying | 100 | - | NO |
| description | text | - | - | NO |
| short_description | character varying | 200 | - | YES |
| price | double precision | - | - | NO |
| duration | integer | - | - | NO |
| image_url | character varying | 256 | - | YES |
| is_available | boolean | - | - | YES |
| created_at | timestamp without time zone | - | - | YES |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `service_pkey` (id)
- UNIQUE INDEX `service_slug_key` (slug)

---

## socialaccount_socialaccount

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| provider | character varying | 200 | - | NO |
| uid | character varying | 191 | - | NO |
| last_login | timestamp with time zone | - | - | NO |
| date_joined | timestamp with time zone | - | - | NO |
| extra_data | jsonb | - | - | NO |
| user_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `user_id` → `auth_user.id`

### Indexes

- UNIQUE INDEX `socialaccount_socialaccount_pkey` (id)
- UNIQUE INDEX `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (provider, uid)
- INDEX `socialaccount_socialaccount_user_id_8146e70c` (user_id)

---

## socialaccount_socialapp

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| provider | character varying | 30 | - | NO |
| name | character varying | 40 | - | NO |
| client_id | character varying | 191 | - | NO |
| secret | character varying | 191 | - | NO |
| key | character varying | 191 | - | NO |
| provider_id | character varying | 200 | - | NO |
| settings | jsonb | - | - | NO |

### Primary Key

- id

### Indexes

- UNIQUE INDEX `socialaccount_socialapp_pkey` (id)

---

## socialaccount_socialapp_sites

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | bigint | - | - | NO |
| socialapp_id | integer | - | - | NO |
| site_id | integer | - | - | NO |

### Primary Key

- id

### Foreign Keys

- `socialapp_id` → `socialaccount_socialapp.id`
- `site_id` → `django_site.id`

### Indexes

- UNIQUE INDEX `socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq` (socialapp_id, site_id)
- UNIQUE INDEX `socialaccount_socialapp_sites_pkey` (id)
- INDEX `socialaccount_socialapp_sites_site_id_2579dee5` (site_id)
- INDEX `socialaccount_socialapp_sites_socialapp_id_97fb6e7d` (socialapp_id)

---

## socialaccount_socialtoken

### Columns

| Column Name | Data Type | Length | Default | Nullable |
|------------|-----------|--------|---------|----------|
| id | integer | - | - | NO |
| token | text | - | - | NO |
| token_secret | text | - | - | NO |
| expires_at | timestamp with time zone | - | - | YES |
| account_id | integer | - | - | NO |
| app_id | integer | - | - | YES |

### Primary Key

- id

### Foreign Keys

- `account_id` → `socialaccount_socialaccount.id`
- `app_id` → `socialaccount_socialapp.id`

### Indexes

- INDEX `socialaccount_socialtoken_account_id_951f210e` (account_id)
- INDEX `socialaccount_socialtoken_app_id_636a42d7` (app_id)
- UNIQUE INDEX `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (account_id, app_id)
- UNIQUE INDEX `socialaccount_socialtoken_pkey` (id)

---

