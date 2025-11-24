from sqlalchemy import create_engine, text

url = "postgresql://Capta7nBlack@localhost:5432/caregivers_db"
engine = create_engine(url)

def run():
    with engine.connect() as conn:
        print("Running Part 2 queries...")

        # 5.1
        print("\nAccepted Appointments (Caregiver -> Member):")
        res = conn.execute(text("""
            SELECT U_CG.given_name || ' ' || U_CG.surname as Caregiver, 
                   U_MEM.given_name || ' ' || U_MEM.surname as Member
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            JOIN "USER" U_CG ON C.caregiver_user_id = U_CG.user_id
            JOIN MEMBER M ON A.member_user_id = M.member_user_id
            JOIN "USER" U_MEM ON M.member_user_id = U_MEM.user_id
            WHERE A.status = 'Accepted';
        """))
        for r in res: print(f" - {r[0]} -> {r[1]}")

        # 5.2
        print("\nJobs requiring 'soft-spoken':")
        res = conn.execute(text("SELECT job_id, other_requirements FROM JOB WHERE other_requirements LIKE '%soft-spoken%';"))
        for r in res: print(f" - Job {r[0]}: {r[1]}")

        # 5.3
        print("\nBabysitter Work Hours:")
        res = conn.execute(text("""
            SELECT A.appointment_id, A.work_hours 
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            WHERE C.caregiving_type = 'babysitter';
        """))
        for r in res: print(f" - Appt {r[0]}: {r[1]} hrs")

        # 5.4
        print("\nMembers in Astana (Elderly Care, No Pets):")
        res = conn.execute(text("""
            SELECT U.given_name, U.surname
            FROM MEMBER M
            JOIN "USER" U ON M.member_user_id = U.user_id
            JOIN JOB J ON M.member_user_id = J.member_user_id
            WHERE U.city = 'Astana' 
              AND J.required_caregiving_type = 'caregiver for elderly'
              AND M.house_rules LIKE '%No pets%';
        """))
        for r in res: print(f" - {r[0]} {r[1]}")

        # 6.1
        print("\nApplicant count per Job:")
        res = conn.execute(text("""
            SELECT J.job_id, COUNT(JA.caregiver_user_id) as count
            FROM JOB J
            LEFT JOIN JOB_APPLICATION JA ON J.job_id = JA.job_id
            GROUP BY J.job_id ORDER BY J.job_id;
        """))
        for r in res: print(f" - Job {r[0]}: {r[1]}")

        # 6.2
        print("\nTotal hours (Accepted):")
        res = conn.execute(text("SELECT SUM(work_hours) FROM APPOINTMENT WHERE status = 'Accepted';"))
        for r in res: print(f" - {r[0]}")

        # 6.3
        print("\nAvg Pay (Accepted):")
        res = conn.execute(text("""
            SELECT AVG(C.hourly_rate * A.work_hours)
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            WHERE A.status = 'Accepted';
        """))
        for r in res: print(f" - ${round(r[0], 2)}")

        # 6.4
        print("\nAbove Average Earners:")
        res = conn.execute(text("""
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
        for r in res: print(f" - {r[0]}: ${r[1]}")

        # 7
        print("\nTotal Revenue:")
        res = conn.execute(text("""
            SELECT SUM(C.hourly_rate * A.work_hours)
            FROM APPOINTMENT A
            JOIN CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
            WHERE A.status = 'Accepted';
        """))
        for r in res: print(f" - ${r[0]}")

        # 8
        print("\nView: job_applicants_view")
        conn.execute(text("""
            CREATE OR REPLACE VIEW job_applicants_view AS
            SELECT J.job_id, U.given_name, JA.date_applied
            FROM JOB_APPLICATION JA
            JOIN "USER" U ON JA.caregiver_user_id = U.user_id
            JOIN JOB J ON JA.job_id = J.job_id;
        """))
        res = conn.execute(text("SELECT * FROM job_applicants_view LIMIT 5;"))
        for r in res: print(f" - {r}")

        print("\nExecuting updates/deletes...")
        
        conn.execute(text("UPDATE \"USER\" SET phone_number = '+77773414141' WHERE given_name = 'Arman' AND surname = 'Armanov';"))
        
        conn.execute(text("""
            UPDATE CAREGIVER
            SET hourly_rate = CASE
                WHEN hourly_rate < 10 THEN hourly_rate + 0.3
                ELSE hourly_rate * 1.10
            END;
        """))

        conn.execute(text("""
            DELETE FROM JOB 
            WHERE member_user_id = (SELECT user_id FROM "USER" WHERE given_name = 'Amina' AND surname = 'Aminova');
        """))

        conn.execute(text("""
            DELETE FROM MEMBER
            WHERE member_user_id IN (SELECT member_user_id FROM ADDRESS WHERE street LIKE '%Kabanbay Batyr%');
        """))

        conn.commit()
        print("Done.")

if __name__ == "__main__":
    run()
