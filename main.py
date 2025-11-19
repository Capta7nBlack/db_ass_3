from sqlalchemy import create_engine, text

# CONFIGURATION (No password)
db_string = "postgresql://Capta7nBlack@localhost:5432/caregivers_db"
engine = create_engine(db_string)

def create_tables():
    with engine.connect() as conn:
        print("1. Creating tables...")
        
        # Create USER table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS "USER" (
                user_id SERIAL PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                given_name VARCHAR(50) NOT NULL,
                surname VARCHAR(50) NOT NULL,
                city VARCHAR(50),
                phone_number VARCHAR(20),
                profile_description TEXT,
                password VARCHAR(100) NOT NULL
            );
        """))

        # Create CAREGIVER table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS CAREGIVER (
                caregiver_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
                photo VARCHAR(255),
                gender VARCHAR(10),
                caregiving_type VARCHAR(50),
                hourly_rate DECIMAL(10, 2)
            );
        """))

        # Create MEMBER table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS MEMBER (
                member_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
                house_rules TEXT,
                dependent_description TEXT
            );
        """))

        # Create ADDRESS table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ADDRESS (
                member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
                house_number VARCHAR(20),
                street VARCHAR(100),
                town VARCHAR(50)
            );
        """))

        # Create JOB table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS JOB (
                job_id SERIAL PRIMARY KEY,
                member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
                required_caregiving_type VARCHAR(50),
                other_requirements TEXT,
                date_posted DATE DEFAULT CURRENT_DATE
            );
        """))

        # Create JOB_APPLICATION table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS JOB_APPLICATION (
                caregiver_user_id INTEGER REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
                job_id INTEGER REFERENCES JOB(job_id) ON DELETE CASCADE,
                date_applied DATE DEFAULT CURRENT_DATE,
                PRIMARY KEY (caregiver_user_id, job_id)
            );
        """))

        # Create APPOINTMENT table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS APPOINTMENT (
                appointment_id SERIAL PRIMARY KEY,
                caregiver_user_id INTEGER REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
                member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
                appointment_date DATE,
                appointment_time TIME,
                work_hours INTEGER,
                status VARCHAR(20) DEFAULT 'Pending'
            );
        """))        


        conn.commit()
        print("   Tables created successfully.")

def seed_data():
    with engine.connect() as conn:
        print("2. Seeding BULK data (10+ per table)...")
        
        # Clearing tables
        conn.execute(text("TRUNCATE TABLE APPOINTMENT, JOB_APPLICATION, JOB, ADDRESS, MEMBER, CAREGIVER, \"USER\" RESTART IDENTITY CASCADE;"))

        # 1. INSERT 22 USERS (Need enough to cover 10 Members + 10 Caregivers)
        users_sql = """
        INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
        -- ORIGINAL DATA (For Queries)
        ('arman@mail.com', 'Arman', 'Armanov', 'Astana', '+77011111111', 'Regular guy', 'pass123'), -- ID 1 (Member)
        ('amina@mail.com', 'Amina', 'Aminova', 'Almaty', '+77022222222', 'Need help', 'pass123'), -- ID 2 (Member)
        ('nanny1@mail.com', 'Sarah', 'Poppins', 'Astana', '+77033333333', 'Pro nanny', 'pass123'), -- ID 3 (CG)
        ('elder1@mail.com', 'John', 'Doe', 'Astana', '+77044444444', 'Experienced nurse', 'pass123'), -- ID 4 (CG)
        ('baby2@mail.com', 'Alice', 'Smith', 'Almaty', '+77055555555', 'Student job', 'pass123'), -- ID 5 (CG)
        ('mem_kab@mail.com', 'Kairat', 'Nurtas', 'Astana', '+77066666666', 'Singer', 'pass123'), -- ID 6 (Member)
        ('mem_ast@mail.com', 'Saule', 'Ivanova', 'Astana', '+77077777777', 'Busy mom', 'pass123'), -- ID 7 (Member)
        ('cg_cheap@mail.com', 'Low', 'Price', 'Astana', '+77088888888', 'Newbie', 'pass123'), -- ID 8 (CG)
        ('cg_exp@mail.com', 'High', 'Price', 'Astana', '+77099999999', 'Expert', 'pass123'), -- ID 9 (CG)
        ('user10@mail.com', 'Test', 'User', 'Shymkent', '+77100000000', 'Test', 'pass123'), -- ID 10
        
        -- EXTRA FILLER DATA (To reach 10+ per table)
        ('mem11@mail.com', 'M11', 'Surname11', 'Astana', '+77000000011', 'Desc', 'pass'), -- ID 11 (Member)
        ('mem12@mail.com', 'M12', 'Surname12', 'Astana', '+77000000012', 'Desc', 'pass'), -- ID 12 (Member)
        ('mem13@mail.com', 'M13', 'Surname13', 'Almaty', '+77000000013', 'Desc', 'pass'), -- ID 13 (Member)
        ('mem14@mail.com', 'M14', 'Surname14', 'Almaty', '+77000000014', 'Desc', 'pass'), -- ID 14 (Member)
        ('mem15@mail.com', 'M15', 'Surname15', 'Almaty', '+77000000015', 'Desc', 'pass'), -- ID 15 (Member)
        ('mem16@mail.com', 'M16', 'Surname16', 'Almaty', '+77000000016', 'Desc', 'pass'), -- ID 16 (Member)
        
        ('cg17@mail.com', 'C17', 'Surname17', 'Astana', '+77000000017', 'Desc', 'pass'), -- ID 17 (CG)
        ('cg18@mail.com', 'C18', 'Surname18', 'Astana', '+77000000018', 'Desc', 'pass'), -- ID 18 (CG)
        ('cg19@mail.com', 'C19', 'Surname19', 'Almaty', '+77000000019', 'Desc', 'pass'), -- ID 19 (CG)
        ('cg20@mail.com', 'C20', 'Surname20', 'Almaty', '+77000000020', 'Desc', 'pass'), -- ID 20 (CG)
        ('cg21@mail.com', 'C21', 'Surname21', 'Almaty', '+77000000021', 'Desc', 'pass'), -- ID 21 (CG)
        ('cg22@mail.com', 'C22', 'Surname22', 'Almaty', '+77000000022', 'Desc', 'pass'); -- ID 22 (CG)
        """
        conn.execute(text(users_sql))

        # 2. INSERT 11 CAREGIVERS
        cg_sql = """
        INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
        (3, 'p1.jpg', 'F', 'babysitter', 15.00),
        (4, 'p2.jpg', 'M', 'caregiver for elderly', 20.00),
        (5, 'p3.jpg', 'F', 'babysitter', 12.00),
        (8, 'p4.jpg', 'M', 'playmate for children', 8.00),
        (9, 'p5.jpg', 'F', 'caregiver for elderly', 25.00),
        -- Extra
        (17, 'p6.jpg', 'M', 'babysitter', 10.00),
        (18, 'p7.jpg', 'F', 'babysitter', 11.00),
        (19, 'p8.jpg', 'M', 'playmate for children', 9.00),
        (20, 'p9.jpg', 'F', 'caregiver for elderly', 18.00),
        (21, 'p10.jpg', 'M', 'babysitter', 14.00),
        (22, 'p11.jpg', 'F', 'playmate for children', 13.00);
        """
        conn.execute(text(cg_sql))

        # 3. INSERT 10 MEMBERS
        mem_sql = """
        INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
        (1, 'No smoking', 'Active toddler'),
        (2, 'Quiet after 9pm', 'Grandmother'),
        (6, 'No pets', '3 kids'),
        (7, 'Cleanliness', 'Newborn baby'),
        -- Extra
        (11, 'None', 'Son'),
        (12, 'None', 'Daughter'),
        (13, 'No guests', 'Twins'),
        (14, 'No shoes', 'Baby'),
        (15, 'Quiet', 'Elderly'),
        (16, 'None', 'Cat and Kid');
        """
        conn.execute(text(mem_sql))

        # 4. INSERT 10 ADDRESSES
        addr_sql = """
        INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
        (1, '10', 'Mangilik El', 'Astana'),
        (2, '5', 'Abay', 'Almaty'),
        (6, '42', 'Kabanbay Batyr', 'Astana'),
        (7, '12', 'Turan', 'Astana'),
        -- Extra
        (11, '1', 'Street A', 'Astana'),
        (12, '2', 'Street B', 'Astana'),
        (13, '3', 'Street C', 'Almaty'),
        (14, '4', 'Street D', 'Almaty'),
        (15, '5', 'Street E', 'Almaty'),
        (16, '6', 'Street F', 'Almaty');
        """
        conn.execute(text(addr_sql))

        # 5. INSERT 10 JOBS

        job_sql = """
        INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
        (2, 'caregiver for elderly', 'Must be soft-spoken', '2025-11-01'),
        (2, 'caregiver for elderly', 'Night shift', '2025-11-02'),
        (1, 'babysitter', 'Urgent', '2025-11-05'),
        (6, 'caregiver for elderly', 'English speaking', '2025-11-10'),
        -- Extra
        (11, 'babysitter', 'Fun', '2025-11-11'),
        (12, 'babysitter', 'Math tutor', '2025-11-12'),
        (13, 'playmate for children', 'Active', '2025-11-13'),
        (14, 'babysitter', 'Weekend', '2025-11-14'),
        (15, 'caregiver for elderly', 'Strong', '2025-11-15'),
        (16, 'playmate for children', 'Gaming', '2025-11-16');
        """
        conn.execute(text(job_sql))

        # 6. INSERT 10 APPLICATIONS
        app_sql = """
        INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
        (4, 1, '2025-11-03'),
        (9, 1, '2025-11-03'),
        (3, 3, '2025-11-06'),
        -- Extra
        (17, 5, '2025-11-12'),
        (18, 6, '2025-11-13'),
        (19, 7, '2025-11-14'),
        (20, 8, '2025-11-15'),
        (21, 9, '2025-11-16'),
        (22, 10, '2025-11-17'),
        (5, 2, '2025-11-04');
        """
        conn.execute(text(app_sql))

        # 7. INSERT 10 APPOINTMENTS
        apt_sql = """
        INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
        (3, 1, '2025-11-20', '14:00', 4, 'Accepted'),
        (4, 2, '2025-11-21', '10:00', 5, 'Accepted'),
        (8, 7, '2025-11-22', '09:00', 2, 'Pending'),
        (5, 6, '2025-11-23', '18:00', 3, 'Accepted'),
        -- Extra
        (17, 11, '2025-11-24', '10:00', 2, 'Accepted'),
        (18, 12, '2025-11-25', '11:00', 3, 'Pending'),
        (19, 13, '2025-11-26', '12:00', 4, 'Accepted'),
        (20, 14, '2025-11-27', '13:00', 5, 'Declined'),
        (21, 15, '2025-11-28', '14:00', 6, 'Accepted'),
        (22, 16, '2025-11-29', '15:00', 2, 'Pending');
        """
        conn.execute(text(apt_sql))

        conn.commit()
        print("   Data seeded successfully (10+ per table).")
if __name__ == "__main__":
    create_tables()
    seed_data()
