import sqlalchemy
from sqlalchemy import create_engine, text

# CONFIGURATION
db_string = "postgresql://caregivers_db_7dm8_user:pKjPqCvuTRFyjTPDEc9noF94yNRb7ZmD@dpg-d4i4i5buibrs73dvgfp0-a/caregivers_db_7dm8"
engine = create_engine(db_string)

def create_tables():
    with engine.connect() as conn:
        print("1. Creating tables...")
        
        # 1. USER
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

        # 2. CAREGIVER
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS CAREGIVER (
                caregiver_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
                photo VARCHAR(255),
                gender VARCHAR(10),
                caregiving_type VARCHAR(50),
                hourly_rate DECIMAL(10, 2)
            );
        """))

        # 3. MEMBER
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS MEMBER (
                member_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
                house_rules TEXT,
                dependent_description TEXT
            );
        """))

        # 4. ADDRESS
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ADDRESS (
                member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
                house_number VARCHAR(20),
                street VARCHAR(100),
                town VARCHAR(50)
            );
        """))

        # 5. JOB
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS JOB (
                job_id SERIAL PRIMARY KEY,
                member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
                required_caregiving_type VARCHAR(50),
                other_requirements TEXT,
                date_posted DATE DEFAULT CURRENT_DATE
            );
        """))

        # 6. JOB_APPLICATION
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS JOB_APPLICATION (
                caregiver_user_id INTEGER REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
                job_id INTEGER REFERENCES JOB(job_id) ON DELETE CASCADE,
                date_applied DATE DEFAULT CURRENT_DATE,
                PRIMARY KEY (caregiver_user_id, job_id)
            );
        """))

        # 7. APPOINTMENT
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
        print("2. Seeding POP CULTURE data...")
        
        # Clear tables
        conn.execute(text("TRUNCATE TABLE APPOINTMENT, JOB_APPLICATION, JOB, ADDRESS, MEMBER, CAREGIVER, \"USER\" RESTART IDENTITY CASCADE;"))

        
        users_sql = """
        INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
        -- [ORIGINAL DATA NEEDED FOR LOGIC]
        ('arman@mail.com', 'Arman', 'Armanov', 'Astana', '+77011111111', 'Regular guy', 'pass123'), -- ID 1
        ('amina@mail.com', 'Amina', 'Aminova', 'Almaty', '+77022222222', 'Need help', 'pass123'), -- ID 2
        ('nanny1@mail.com', 'Sarah', 'Poppins', 'Astana', '+77033333333', 'Pro nanny', 'pass123'), -- ID 3
        ('elder1@mail.com', 'John', 'Doe', 'Astana', '+77044444444', 'Experienced nurse', 'pass123'), -- ID 4
        ('baby2@mail.com', 'Alice', 'Smith', 'Almaty', '+77055555555', 'Student job', 'pass123'), -- ID 5
        ('mem_kab@mail.com', 'Kairat', 'Nurtas', 'Astana', '+77066666666', 'Singer', 'pass123'), -- ID 6
        ('mem_ast@mail.com', 'Saule', 'Ivanova', 'Astana', '+77077777777', 'Busy mom', 'pass123'), -- ID 7
        ('cg_cheap@mail.com', 'Low', 'Price', 'Astana', '+77088888888', 'Newbie', 'pass123'), -- ID 8
        ('cg_exp@mail.com', 'High', 'Price', 'Astana', '+77099999999', 'Expert', 'pass123'), -- ID 9
        ('user10@mail.com', 'Test', 'User', 'Shymkent', '+77100000000', 'Test', 'pass123'), -- ID 10
        
        ('ironman@stark.com', 'Tony', 'Stark', 'Malibu', '+10000000001', 'Billionaire philanthropist', 'jarvis'), -- ID 11
        ('bateman@pierce.com', 'Patrick', 'Bateman', 'New York', '+10000000002', 'Into mergers and acquisitions', 'paulallen'), -- ID 12
        ('sherlock@baker.com', 'Sherlock', 'Holmes', 'London', '+44000000001', 'Consulting Detective', 'watson'), -- ID 13
        ('django@unchained.com', 'Django', 'Freeman', 'Mississippi', '+15555555555', 'The fastest gun', 'freedom'), -- ID 14
        ('onizuka@gto.com', 'Eikichi', 'Onizuka', 'Tokyo', '+81000000001', 'Great Teacher', 'bike'), -- ID 15
        ('san@mononoke.com', 'San', 'Princess', 'Forest', '+81000000002', 'Raised by wolves', 'moro'), -- ID 16
        
        ('gon@hunter.com', 'Gon', 'Freecss', 'Whale Island', '+81000000003', 'Very energetic and strong', 'rock'), -- ID 17
        ('killua@zoldyck.com', 'Killua', 'Zoldyck', 'Kukuroo', '+81000000004', 'Professional assassin skills', 'lightning'), -- ID 18
        ('toji@fushiguro.com', 'Toji', 'Fushiguro', 'Tokyo', '+81000000005', 'Sorcerer Killer, works for money', 'zenin'), -- ID 19
        ('watson@baker.com', 'John', 'Watson', 'London', '+44000000002', 'Former army doctor', 'mary'), -- ID 20
        ('eboshi@iron.com', 'Lady', 'Eboshi', 'Iron Town', '+81000000006', 'Leader of Iron Town', 'leper'), -- ID 21
        ('ashitaka@emishi.com', 'Ashitaka', 'Prince', 'Emishi', '+81000000007', 'Cursed prince', 'yakul'); -- ID 22
        """
        conn.execute(text(users_sql))

        cg_sql = """
        INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
        (3, 'p1.jpg', 'F', 'babysitter', 15.00),
        (4, 'p2.jpg', 'M', 'caregiver for elderly', 20.00),
        (5, 'p3.jpg', 'F', 'babysitter', 12.00),
        (8, 'p4.jpg', 'M', 'playmate for children', 8.00),
        (9, 'p5.jpg', 'F', 'caregiver for elderly', 25.00),
        
        (17, 'gon.jpg', 'M', 'playmate for children', 10.00), -- Gon (Cheap and fun)
        (18, 'killua.jpg', 'M', 'playmate for children', 50.00), -- Killua (Premium bodyguard/playmate)
        (19, 'toji.jpg', 'M', 'babysitter', 100.00), -- Toji (Expensive, needs cash)
        (20, 'watson.jpg', 'M', 'caregiver for elderly', 30.00), -- Watson (Doctor, good for elderly)
        (21, 'eboshi.jpg', 'F', 'caregiver for elderly', 40.00), -- Eboshi (Takes care of the sick)
        (22, 'ashitaka.jpg', 'M', 'playmate for children', 15.00); -- Ashitaka (Responsible)
        """
        conn.execute(text(cg_sql))

        mem_sql = """
        INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
        (1, 'No smoking', 'Active toddler'),
        (2, 'Quiet after 9pm', 'Grandmother needs help'),
        (6, 'No pets', '3 kids'),
        (7, 'Cleanliness', 'Newborn baby'),
        
        (11, 'Do not touch my suits', 'Morgan Stark (Daughter)'), -- Tony Stark
        (12, 'Must like Phil Collins', 'No dependents, just cleaning'), -- Patrick Bateman
        (13, 'No loud noises', 'Mrs. Hudson (Landlady)'), -- Sherlock
        (14, 'Freedom above all', 'Broomhilda (Wife)'), -- Django
        (15, 'Respect the bike', 'Problematic students'), -- Onizuka
        (16, 'Protect the forest', 'Wolf pups'); -- San
        """
        conn.execute(text(mem_sql))

        # 4. INSERT ADDRESSES
        addr_sql = """
        INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
        (1, '10', 'Mangilik El', 'Astana'),
        (2, '5', 'Abay', 'Almaty'),
        (6, '42', 'Kabanbay Batyr', 'Astana'),
        (7, '12', 'Turan', 'Astana'),
        
        (11, '10880', 'Malibu Point', 'California'), -- Stark
        (12, '55', 'West 81st Street', 'New York'), -- Bateman
        (13, '221B', 'Baker Street', 'London'), -- Sherlock
        (14, '1', 'Candyland', 'Mississippi'), -- Django
        (15, '3-4', 'Kichijoji', 'Tokyo'), -- Onizuka
        (16, '99', 'Iron Town Road', 'Forest'); -- San
        """
        conn.execute(text(addr_sql))

        # 5. INSERT JOBS
        job_sql = """
        INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
        (2, 'caregiver for elderly', 'Must be soft-spoken', '2025-11-01'),
        (2, 'caregiver for elderly', 'Night shift', '2025-11-02'),
        (1, 'babysitter', 'Urgent', '2025-11-05'),
        (6, 'caregiver for elderly', 'English speaking', '2025-11-10'),
        
        (11, 'babysitter', 'Must understand quantum physics', '2025-11-11'), -- Stark needs smart babysitter
        (12, 'caregiver for elderly', 'Must handle cleaning well', '2025-11-12'), -- Bateman
        (13, 'caregiver for elderly', 'Must tolerate violin practice', '2025-11-13'), -- Sherlock
        (14, 'playmate for children', 'Teach them to ride horses', '2025-11-14'), -- Django
        (15, 'playmate for children', 'Must be tough', '2025-11-15'), -- Onizuka
        (16, 'caregiver for elderly', 'Must respect nature', '2025-11-16'); -- San
        """
        conn.execute(text(job_sql))

        # 6. INSERT APPLICATIONS
        app_sql = """
        INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
        (4, 1, '2025-11-03'),
        (9, 1, '2025-11-03'),
        (3, 3, '2025-11-06'),
        
        (17, 5, '2025-11-12'), -- Gon applies to Stark's job
        (18, 5, '2025-11-13'), -- Killua applies to Stark's job
        (19, 9, '2025-11-14'), -- Toji applies to Onizuka's job
        (20, 7, '2025-11-15'), -- Watson applies to Sherlock's job
        (21, 6, '2025-11-16'), -- Eboshi applies to Bateman's job
        (22, 8, '2025-11-17'), -- Ashitaka applies to Django's job
        (5, 2, '2025-11-04');
        """
        conn.execute(text(app_sql))

        # 7. INSERT APPOINTMENTS
        apt_sql = """
        INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
        (3, 1, '2025-11-20', '14:00', 4, 'Accepted'),
        (4, 2, '2025-11-21', '10:00', 5, 'Accepted'),
        (8, 7, '2025-11-22', '09:00', 2, 'Pending'),
        (5, 6, '2025-11-23', '18:00', 3, 'Accepted'),
        
        (17, 11, '2025-11-24', '10:00', 2, 'Accepted'), -- Gon works for Tony Stark
        (18, 12, '2025-11-25', '11:00', 3, 'Pending'),  -- Killua pending for Bateman
        (20, 13, '2025-11-26', '12:00', 4, 'Accepted'), -- Watson works for Sherlock
        (19, 14, '2025-11-27', '13:00', 5, 'Declined'), -- Toji declined by Django
        (22, 16, '2025-11-28', '14:00', 6, 'Accepted'), -- Ashitaka works for San
        (21, 15, '2025-11-29', '15:00', 2, 'Pending');  -- Eboshi pending for Onizuka
        """
        conn.execute(text(apt_sql))

        conn.commit()
        print("   Data seeded successfully (Pop Culture Edition).")

if __name__ == "__main__":
    create_tables()
    seed_data()
