-- MetaMystic Database Schema (Generated from Django Models)

-- Model: Profile (Table: astrology_profile)
CREATE TABLE IF NOT EXISTS "astrology_profile" (
    "id" serial NOT NULL PRIMARY KEY ,
    "user_id" integer NOT NULL ,
    "phone_number" varchar(128) ,
    "birth_date" date ,
    "birth_time" time ,
    "birth_place" varchar(100) ,
    "bio" text ,
    "profile_image" varchar(100) ,
    "is_phone_verified" boolean NOT NULL ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL ,
    CONSTRAINT "astrology_profile_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_profile" IS '
    Extended user profile model
    ';

-- Model: OTP (Table: astrology_otp)
CREATE TABLE IF NOT EXISTS "astrology_otp" (
    "id" serial NOT NULL PRIMARY KEY ,
    "user_id" integer NOT NULL ,
    "otp_code" varchar(6) NOT NULL ,
    "is_used" boolean NOT NULL ,
    "created_at" date NOT NULL ,
    "expires_at" date NOT NULL ,
    CONSTRAINT "astrology_otp_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_otp" IS '
    OTP model for phone verification
    ';

-- Model: Service (Table: astrology_service)
CREATE TABLE IF NOT EXISTS "astrology_service" (
    "id" serial NOT NULL PRIMARY KEY ,
    "name" varchar(100) NOT NULL ,
    "slug" varchar(50) NOT NULL ,
    "description" text NOT NULL ,
    "short_description" varchar(200) NOT NULL ,
    "price" decimal(6, 2) NOT NULL ,
    "duration" integer NOT NULL ,
    "image" varchar(100) ,
    "is_available" boolean NOT NULL ,
    "created_at" date NOT NULL 
);

COMMENT ON TABLE "astrology_service" IS '
    Astrology consultation service model
    ';

-- Model: AvailabilitySlot (Table: astrology_availabilityslot)
CREATE TABLE IF NOT EXISTS "astrology_availabilityslot" (
    "id" serial NOT NULL PRIMARY KEY ,
    "day_of_week" integer NOT NULL ,
    "start_time" time NOT NULL ,
    "end_time" time NOT NULL ,
    "is_active" boolean NOT NULL 
);

COMMENT ON TABLE "astrology_availabilityslot" IS '
    Model for defining available time slots for bookings
    ';

-- Model: BlockedDate (Table: astrology_blockeddate)
CREATE TABLE IF NOT EXISTS "astrology_blockeddate" (
    "id" serial NOT NULL PRIMARY KEY ,
    "date" date NOT NULL ,
    "reason" varchar(255) NOT NULL 
);

COMMENT ON TABLE "astrology_blockeddate" IS '
    Model for blocked dates when no bookings are allowed
    ';

-- Model: Booking (Table: astrology_booking)
CREATE TABLE IF NOT EXISTS "astrology_booking" (
    "id" serial NOT NULL PRIMARY KEY ,
    "user_id" integer ,
    "service_id" integer NOT NULL ,
    "booking_date" date NOT NULL ,
    "booking_time" time NOT NULL ,
    "customer_name" varchar(100) NOT NULL ,
    "customer_email" varchar(254) NOT NULL ,
    "customer_phone" varchar(128) NOT NULL ,
    "notes" text ,
    "status" varchar(20) NOT NULL ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL ,
    "is_guest_booking" boolean NOT NULL ,
    "registration_link_sent" boolean NOT NULL ,
    CONSTRAINT "astrology_booking_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE CASCADE ,
    CONSTRAINT "astrology_booking_service_id_fkey" FOREIGN KEY ("service_id") REFERENCES "astrology_service" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_booking" IS '
    Booking model for astrology consultations
    ';

-- Model: BlogPost (Table: astrology_blogpost)
CREATE TABLE IF NOT EXISTS "astrology_blogpost" (
    "id" serial NOT NULL PRIMARY KEY ,
    "title" varchar(120) NOT NULL ,
    "slug" varchar(50) NOT NULL ,
    "summary" varchar(200) NOT NULL ,
    "content" text NOT NULL ,
    "image" varchar(100) ,
    "author_id" integer NOT NULL ,
    "published" boolean NOT NULL ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL ,
    CONSTRAINT "astrology_blogpost_author_id_fkey" FOREIGN KEY ("author_id") REFERENCES "auth_user" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_blogpost" IS '
    Blog post model
    ';

-- Model: Coupon (Table: astrology_coupon)
CREATE TABLE IF NOT EXISTS "astrology_coupon" (
    "id" serial NOT NULL PRIMARY KEY ,
    "code" varchar(20) NOT NULL ,
    "description" varchar(100) NOT NULL ,
    "discount_percentage" integer ,
    "discount_amount" decimal(6, 2) ,
    "valid_from" date NOT NULL ,
    "valid_to" date NOT NULL ,
    "min_purchase_amount" decimal(6, 2) ,
    "max_uses" integer ,
    "used_count" integer NOT NULL ,
    "is_active" boolean NOT NULL ,
    "created_at" date NOT NULL 
);

COMMENT ON TABLE "astrology_coupon" IS '
    Coupon code model for discounts
    ';

-- Model: CartItem (Table: astrology_cartitem)
CREATE TABLE IF NOT EXISTS "astrology_cartitem" (
    "id" serial NOT NULL PRIMARY KEY ,
    "session_id" varchar(64) NOT NULL ,
    "service_id" integer NOT NULL ,
    "quantity" integer NOT NULL ,
    "created_at" date NOT NULL ,
    CONSTRAINT "astrology_cartitem_service_id_fkey" FOREIGN KEY ("service_id") REFERENCES "astrology_service" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_cartitem" IS '
    Shopping cart item model
    ';

-- Model: Order (Table: astrology_order)
CREATE TABLE IF NOT EXISTS "astrology_order" (
    "id" serial NOT NULL PRIMARY KEY ,
    "order_number" varchar(20) NOT NULL ,
    "user_id" integer ,
    "customer_name" varchar(100) NOT NULL ,
    "customer_email" varchar(254) NOT NULL ,
    "customer_phone" varchar(128) ,
    "subtotal_amount" decimal(8, 2) NOT NULL ,
    "discount_amount" decimal(8, 2) NOT NULL ,
    "total_amount" decimal(8, 2) NOT NULL ,
    "coupon_id" integer ,
    "payment_method" varchar(20) NOT NULL ,
    "payment_id" varchar(100) ,
    "status" varchar(20) NOT NULL ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL ,
    CONSTRAINT "astrology_order_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE SET NULL ,
    CONSTRAINT "astrology_order_coupon_id_fkey" FOREIGN KEY ("coupon_id") REFERENCES "astrology_coupon" ("id") ON DELETE SET NULL 
);

COMMENT ON TABLE "astrology_order" IS '
    Order model
    ';

-- Model: OrderItem (Table: astrology_orderitem)
CREATE TABLE IF NOT EXISTS "astrology_orderitem" (
    "id" serial NOT NULL PRIMARY KEY ,
    "order_id" integer NOT NULL ,
    "service_id" integer ,
    "service_name" varchar(100) NOT NULL ,
    "price" decimal(8, 2) NOT NULL ,
    "quantity" integer NOT NULL ,
    CONSTRAINT "astrology_orderitem_order_id_fkey" FOREIGN KEY ("order_id") REFERENCES "astrology_order" ("id") ON DELETE CASCADE ,
    CONSTRAINT "astrology_orderitem_service_id_fkey" FOREIGN KEY ("service_id") REFERENCES "astrology_service" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_orderitem" IS '
    Order item model
    ';

-- Model: Contact (Table: astrology_contact)
CREATE TABLE IF NOT EXISTS "astrology_contact" (
    "id" serial NOT NULL PRIMARY KEY ,
    "name" varchar(100) NOT NULL ,
    "email" varchar(254) NOT NULL ,
    "subject" varchar(200) NOT NULL ,
    "message" text NOT NULL ,
    "is_read" boolean NOT NULL ,
    "created_at" date NOT NULL 
);

COMMENT ON TABLE "astrology_contact" IS '
    Contact form submission model
    ';

-- Model: UserReading (Table: astrology_userreading)
CREATE TABLE IF NOT EXISTS "astrology_userreading" (
    "id" serial NOT NULL PRIMARY KEY ,
    "user_id" integer NOT NULL ,
    "title" varchar(100) NOT NULL ,
    "content" text NOT NULL ,
    "reading_date" date NOT NULL ,
    "is_public" boolean NOT NULL ,
    "pdf_report" varchar(100) ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL ,
    CONSTRAINT "astrology_userreading_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_userreading" IS '
    User astrology reading model
    ';

-- Model: ConsultationReport (Table: astrology_consultationreport)
CREATE TABLE IF NOT EXISTS "astrology_consultationreport" (
    "id" serial NOT NULL PRIMARY KEY ,
    "user_id" integer NOT NULL ,
    "title" varchar(100) NOT NULL ,
    "description" text ,
    "report_file" varchar(100) NOT NULL ,
    "consultation_date" date NOT NULL ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL ,
    CONSTRAINT "astrology_consultationreport_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE CASCADE 
);

COMMENT ON TABLE "astrology_consultationreport" IS '
    Consultation reports model for PDF uploads
    ';

-- Model: WhatsAppConfig (Table: astrology_whatsappconfig)
CREATE TABLE IF NOT EXISTS "astrology_whatsappconfig" (
    "id" serial NOT NULL PRIMARY KEY ,
    "phone_number" varchar(128) NOT NULL ,
    "default_message" varchar(255) NOT NULL ,
    "display_name" varchar(100) NOT NULL ,
    "is_active" boolean NOT NULL ,
    "created_at" date NOT NULL ,
    "updated_at" date NOT NULL 
);

COMMENT ON TABLE "astrology_whatsappconfig" IS '
    WhatsApp configuration for chat integration
    ';


-- Database Summary:
-- Total Models/Tables: 0
