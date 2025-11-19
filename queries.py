from sqlalchemy import create_engine, text

# CONFIGURATION
db_string = "postgresql://Capta7nBlack@localhost:5432/caregivers_db"
engine = create_engine(db_string)

def run_queries():
    with engine.connect() as conn:
        print("="*50)
        print("PART 2: SQL QUERIES EXECUTION")
        print("="*50)

        # ==========================================
        # SECTION A: READ OPERATIONS (Items 5, 6, 7, 8)
        # We run these FIRST to ensure we have data to show
        # before we delete it in the next steps.
        # ==========================================

        print("\n--- 5. SIMPLE QUERIES ---")
        
        print("5.1 Caregiver & Member names for Accepted Appointments:")
        result = conn.execute(text("""
            SELECT U_CG.given_name || ' ' || U_CG.surname as Caregiver, 
                   U_MEM.given_name || ' ' || U_MEM.surname as Member
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            JOIN "USER" U_CG ON C.caregiver_user_id = U_CG.user_id
            JOIN MEMBER M ON A.member_user_id = M.member_user_id
            JOIN "USER" U_MEM ON M.member_user_id = U_MEM.user_id
            WHERE A.status = 'Accepted';
        """))
        for row in result: print(f"   - {row[0]} -> {row[1]}")

        print("\n5.2 Job IDs with 'soft-spoken' in requirements:")
        result = conn.execute(text("SELECT job_id, other_requirements FROM JOB WHERE other_requirements LIKE '%soft-spoken%';"))
        for row in result: print(f"   - Job ID: {row[0]} ({row[1]})")

        print("\n5.3 Work hours of all babysitter positions:")
        result = conn.execute(text("""
            SELECT A.appointment_id, A.work_hours 
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            WHERE C.caregiving_type = 'babysitter';
        """))
        for row in result: print(f"   - Appt {row[0]}: {row[1]} hours")

        print("\n5.4 Members looking for Elderly Care in Astana with 'No pets' rule:")
        result = conn.execute(text("""
            SELECT U.given_name, U.surname
            FROM MEMBER M
            JOIN "USER" U ON M.member_user_id = U.user_id
            JOIN JOB J ON M.member_user_id = J.member_user_id
            WHERE U.city = 'Astana' 
              AND J.required_caregiving_type = 'caregiver for elderly'
              AND M.house_rules LIKE '%No pets%';
        """))
        for row in result: print(f"   - {row[0]} {row[1]}")


        print("\n--- 6. COMPLEX QUERIES ---")

        print("6.1 Count applicants for each job:")
        result = conn.execute(text("""
            SELECT J.job_id, COUNT(JA.caregiver_user_id) as count
            FROM JOB J
            LEFT JOIN JOB_APPLICATION JA ON J.job_id = JA.job_id
            GROUP BY J.job_id ORDER BY J.job_id;
        """))
        for row in result: print(f"   - Job {row[0]}: {row[1]} applicants")

        print("\n6.2 Total hours spent by caregivers (Accepted Appts):")
        result = conn.execute(text("SELECT SUM(work_hours) FROM APPOINTMENT WHERE status = 'Accepted';"))
        for row in result: print(f"   - Total: {row[0]} hours")

        print("\n6.3 Average pay of caregivers (Accepted Appts):")
        # Calculation: Average of (Hourly Rate * Work Hours)
        result = conn.execute(text("""
            SELECT AVG(C.hourly_rate * A.work_hours)
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            WHERE A.status = 'Accepted';
        """))
        for row in result: print(f"   - Average Pay per Appt: ${round(row[0], 2)}")

        print("\n6.4 Caregivers earning above average:")
        result = conn.execute(text("""
            SELECT U.given_name, SUM(C.hourly_rate * A.work_hours) as total_earned
            FROM CAREGIVER C
            JOIN "USER" U ON C.caregiver_user_id = U.user_id
            JOIN APPOINTMENT A ON C.caregiver_user_id = A.caregiver_user_id
            WHERE A.status = 'Accepted'
            GROUP BY U.given_name, U.surname
            HAVING SUM(C.hourly_rate * A.work_hours) > (
                SELECT AVG(C2.hourly_rate * A2.work_hours)
                FROM APPOINTMENT A2
                JOIN CAREGIVER C2 ON A2.caregiver_user_id = C2.caregiver_user_id
                WHERE A2.status = 'Accepted'
            );
        """))
        for row in result: print(f"   - {row[0]}: ${row[1]}")


        print("\n--- 7. DERIVED ATTRIBUTE ---")
        print("Total cost of all accepted appointments:")
        result = conn.execute(text("""
            SELECT SUM(C.hourly_rate * A.work_hours)
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            WHERE A.status = 'Accepted';
        """))
        for row in result: print(f"   - Total Revenue: ${row[0]}")


        print("\n--- 8. VIEW OPERATION ---")
        print("Creating and selecting from 'job_applicants_view':")
        conn.execute(text("""
            CREATE OR REPLACE VIEW job_applicants_view AS
            SELECT J.job_id, U.given_name, JA.date_applied
            FROM JOB_APPLICATION JA
            JOIN "USER" U ON JA.caregiver_user_id = U.user_id
            JOIN JOB J ON JA.job_id = J.job_id;
        """))
        result = conn.execute(text("SELECT * FROM job_applicants_view LIMIT 5;"))
        for row in result: print(f"   - {row}")


        # ==========================================
        # SECTION B: UPDATE/DELETE OPERATIONS (Items 3, 4)
        # We do these LAST so we don't break the queries above.
        # ==========================================

        print("\n" + "="*30)
        print("EXECUTING UPDATES AND DELETES")
        print("="*30)

        print("3.1 Updating phone number for Arman Armanov...")
        conn.execute(text("UPDATE \"USER\" SET phone_number = '+77773414141' WHERE given_name = 'Arman' AND surname = 'Armanov';"))
        
        print("3.2 Updating Commission Fees (logic: <10 add 0.3, else +10%)...")
        conn.execute(text("""
            UPDATE CAREGIVER
            SET hourly_rate = CASE
                WHEN hourly_rate < 10 THEN hourly_rate + 0.3
                ELSE hourly_rate * 1.10
            END;
        """))

        print("4.1 Deleting jobs posted by Amina Aminova...")
        conn.execute(text("""
            DELETE FROM JOB 
            WHERE member_user_id = (SELECT user_id FROM "USER" WHERE given_name = 'Amina' AND surname = 'Aminova');
        """))

        print("4.2 Deleting members who live on 'Kabanbay Batyr'...")
        conn.execute(text("""
            DELETE FROM MEMBER
            WHERE member_user_id IN (SELECT member_user_id FROM ADDRESS WHERE street LIKE '%Kabanbay Batyr%');
        """))

        conn.commit()
        print("Updates and Deletes committed successfully.")
        print("End of Part 2.")

if __name__ == "__main__":
    run_queries()
