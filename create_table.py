import psycopg2
from faker import Faker
import random

# Function to establish connection to PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="ATSDUMMY1",
            user="postgres",
            password="Chirayu@123",
            host="localhost",
            port="5432"
        )
        print("Connected to the database successfully!")
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
        conn.close()
        return None

def generate_job_description(field):
    # descriptions = {
    #     'Engineering': 'Responsible for developing and designing engineering systems, must have a solid understanding of physics, mathematics, and software development.',
    #     'Human Resource': 'Oversees employee relations, payroll, benefits, and training. Must have excellent communication skills and understanding of labor laws.',
    #     'Finance': 'Manages the company\'s financial planning, risk management, and accounting practices. Knowledge of financial statutes and market analysis is essential.',
    #     'Education': 'Designs and implements educational programs and curricula. Must have a deep understanding of teaching methodologies and student engagement strategies.'
    # }
    descriptions = {
        1: 'Responsible for developing and designing engineering systems, must have a solid understanding of physics, mathematics, and software development.',
        2: 'Oversees employee relations, payroll, benefits, and training. Must have excellent communication skills and understanding of labor laws.',
        3: 'Manages the company\'s financial planning, risk management, and accounting practices. Knowledge of financial statutes and market analysis is essential.',
        4: 'Designs and implements educational programs and curricula. Must have a deep understanding of teaching methodologies and student engagement strategies.'
    }
    return descriptions.get(field, 'General job responsibilities not defined.')

# Function to generate a unique 6-digit application ID
def generate_unique_application_id(existing_ids):
    while True:
        application_id = random.randint(100000, 999999)  # Generate a 6-digit number
        if application_id not in existing_ids:
            return application_id

def generate_unique_interview_id(existing_ids):
    while True:
        interviewer_id = random.randint(10000, 99999)  # Generate a 5-digit number
        if interviewer_id not in existing_ids:
            return interviewer_id

# Function to create tables
def create_tables(conn):
    cur = conn.cursor()
    try:
        
        cur.execute(""" 
        CREATE TABLE IF NOT EXISTS Fields (
            fieldId Serial PRIMARY KEY,
            fieldName VARCHAR NOT NULL UNIQUE
        ); 
        """)
        cur.execute("""
            INSERT INTO Fields (fieldName) VALUES
            ('Engineering'),
            ('Human Resource'),
            ('Finance'),
            ('Education');
        """)

        # Create Applicant table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Applicant (
            email VARCHAR PRIMARY KEY,
            fieldId Integer REFERENCES Fields(fieldId) ON DELETE CASCADE,  
            legalName VARCHAR NOT NULL,
            password VARCHAR NOT NULL,
            Address VARCHAR NOT NULL,
            skills VARCHAR,
            yearOfExperience INTEGER DEFAULT 0,
            workSetting VARCHAR
        );
        """)
        # Create Companies table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Companies (
            companyId VARCHAR PRIMARY KEY,
            password VARCHAR NOT NULL,
            companyName VARCHAR NOT NULL,
            location VARCHAR NOT NULL,
            companyEmail VARCHAR NOT NULL
        );
        """)
        # Create Jobs table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Jobs (
            jobId SERIAL PRIMARY KEY,
            companyId VARCHAR REFERENCES Companies(companyId) ON DELETE CASCADE,
            fieldId Integer REFERENCES Fields(fieldId) ON DELETE CASCADE,   
            jobTitle VARCHAR NOT NULL,
            jobDescription VARCHAR,
            requiredYOE VARCHAR,
            requiredSkills VARCHAR,
            requiredWorkSetting VARCHAR,
            postedDate DATE DEFAULT CURRENT_DATE,
            isActive BOOLEAN DEFAULT TRUE
        );
        """)


        # Create Applications table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Applications (
            applicationId SERIAL PRIMARY KEY,
            email VARCHAR REFERENCES Applicant(email) ON DELETE CASCADE,
            jobId INTEGER REFERENCES Jobs(jobId) ON DELETE CASCADE,
            isShortlisted Boolean DEFAULT FALSE,
            currentStatus VARCHAR DEFAULT 'Applied',
            UNIQUE(email, jobId)
        );
        """)
        # Create Interviewer table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Interviewer (
            InterviewId SERIAL PRIMARY KEY,
            companyId VARCHAR REFERENCES Companies(companyId) ON DELETE CASCADE,
            interviewerName VARCHAR NOT NULL,
            fieldExpertise VARCHAR NOT NULL
        );
        """)
        # Create Interview table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Interview (
            applicationId INTEGER REFERENCES Applications(applicationId) ON DELETE CASCADE,
            interviewerId INTEGER REFERENCES Interviewer(InterviewId) ON DELETE CASCADE,
            isSelected INTEGER DEFAULT 1,
            PRIMARY KEY (applicationId, interviewerId)
        );
        """)
        conn.commit()
        print("Tables created successfully!")
    except psycopg2.Error as e:
        print("Error creating tables.")
        print(e)

# Function to generate and insert minimum required tuples into tables
def generate_and_insert_data(conn, min_applicants=5000, min_companies=40, min_jobs_per_company=10, min_interviewers_per_company=2):
    cur = conn.cursor()
    faker = Faker()


    existing_usernames = set()
    cur.execute("SELECT email FROM Applicant")
    for row in cur.fetchall():
        existing_usernames.add(row[0])
    
    while len(existing_usernames) < min_applicants:
        email = faker.unique.email()
        if email in existing_usernames:
            continue
        existing_usernames.add(email)

        legal_name = faker.name()
        password = faker.password()
        # email = faker.email()
        address = faker.address().replace('\n', ', ')
        # field = random.choice(['Engineering', 'Human Resource', 'Finance', 'Education'])
        field = random.choice([1, 2, 3, 4])

        # Conditional logic to set skills based on the field
        if field == 1:
            skills = random.choice(['C++ and Agile', 'Java and Software Development life cycle', 'Python and Automation testing', 'Javascript and Clound computing'])
        elif field == 2:
            skills = random.choice(['Strategic thinking and LinkedIn recruiter', 'Email Writing and Collaborative', 'Strong Communication and Jira', 'Interpersonal and Human resource information'])
        elif field == 3:
            skills = random.choice(['Accounting and Financial modeling', 'Data Analysis and Budgeting', 'SAP and cash flow management', 'MS Office and Risk analysis'])
        else:  # Education
            skills = random.choice(['Mathematics and Curriculum Expertise', 'Computer Science and Critical thinking', 'Physics and Research abilities', 'Pharmacy and Lab experience'])
        year_of_experience = random.randint(1, 10)
        work_preference = random.choice(['Hybrid', 'Remote', 'Onsite'])
        cur.execute("""
        INSERT INTO Applicant (email, legalName, password, Address, fieldId, skills, yearOfExperience, workSetting) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (email, legal_name, password, address, field, skills, year_of_experience, work_preference))

    # Initialize a set to track existing company names
    existing_company_names = set()
    cur.execute("SELECT companyName FROM Companies")
    for row in cur.fetchall():
        existing_company_names.add(row[0].lower())  # Use lower case to ensure case-insensitive comparison

    for _ in range(min_companies):
        while True:
            company_name = faker.company()
            # Ensure the generated company name is unique
            if company_name.lower() not in existing_company_names:
                break
        
        existing_company_names.add(company_name.lower())  # Add the new company name to the set
        company_id = faker.unique.lexify(text="???").upper()
        password = faker.password()
        location = faker.city() + ", " + faker.state()
        company_email = faker.company_email()
        cur.execute("""
        INSERT INTO Companies (companyId, password, companyName, location, companyEmail) 
        VALUES (%s, %s, %s, %s, %s)
        """, (company_id, password, company_name, location, company_email))

    cur.execute("SELECT companyId FROM Companies")
    company_ids = [record[0] for record in cur.fetchall()]
    for company_id in company_ids:
        for _ in range(random.randint(min_jobs_per_company, min_jobs_per_company + 2)):
            job_title = faker.job()
            required_yoe = str(random.randint(1, 10))
            # required_field = random.choice(['Engineering', 'Human Resource', 'Finance', 'Education'])
            required_field = random.choice([1, 2, 3, 4])
            # Conditional logic to set required_skills based on the required_field
            if required_field == 1:
                required_skills = random.choice(['C++ and Agile', 'Java and Software Development life cycle', 'Python and Automation testing', 'Javascript and Cloud computing'])
                job_title = random.choice(['Software Engineer','Member of Technical Staff'])
            elif required_field == 2:
                required_skills = random.choice(['Strategic thinking and LinkedIn recruiter', 'Email Writing and Collaborative', 'Strong Communication and Jira', 'Interpersonal and Human resource information'])
                job_title = random.choice(['HR Manager', 'Talent Acquisition Specialist', 'Employee Relations Specialist', 'Compensation and Benefits Manager'])
            elif required_field == 3:
                required_skills = random.choice(['Accounting and Financial modeling', 'Data Analysis and Budgeting', 'SAP and cash flow management', 'MS Office and Risk analysis'])
                job_title = random.choice(['Financial Analyst', 'Accountant', 'Investment Banker', 'Charted Financial Consultant'])
            else:
                required_skills = random.choice(['Mathematics and Curriculum Expertise', 'Computer Science and Critical thinking', 'Physics and Research abilities', 'Pharmacy and Lab experience'])
                job_title = random.choice(['Subject Professor', 'Curricullum Developer', 'Educational Consultant', 'STEM Instructor'])

            job_description = generate_job_description(required_field)
            required_work_preference = random.choice(['Hybrid', 'Remote', 'Onsite'])
            posted_date = faker.date_between(start_date="-1y", end_date="today")
            is_active = faker.boolean(chance_of_getting_true=80)
            cur.execute("""
            INSERT INTO Jobs (companyId, jobTitle, jobDescription, requiredYOE, requiredSkills, requiredWorkSetting, fieldId, postedDate, isActive) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (company_id, job_title, job_description, required_yoe, required_skills, required_work_preference, required_field, posted_date, is_active))

# Assuming cur has been defined and connected to your database
    existing_application_ids = set()

    cur.execute("""
    SELECT jobId, requiredYOE,  fieldId, requiredSkills, requiredWorkSetting FROM Jobs where isActive= 'true'
    """)
    jobs = cur.fetchall()

    for job in jobs:
        job_id, required_yoe, required_field, required_skills, required_work_preference = job
        
        cur.execute("""
        SELECT email FROM Applicant
        WHERE 
            ABS(yearOfExperience - %s) <= 1 AND
            fieldId = %s AND
            skills = %s AND
            workSetting = %s
        """, (required_yoe, required_field, required_skills, required_work_preference))
        
        matching_applicants = [row[0] for row in cur.fetchall()]
        
        for email in matching_applicants:
            application_id = generate_unique_application_id(existing_application_ids)
            existing_application_ids.add(application_id)  # Keep track of used IDs
            
            current_status = 'Applied'
            isShortlisted = random.choices([True, False], weights=[70, 30], k=1)[0]
            cur.execute("""
            INSERT INTO Applications (applicationId, email, jobId, isShortlisted,currentStatus) 
            VALUES (%s, %s, %s, %s, %s)
            """, (application_id, email, job_id, isShortlisted, current_status))

    field_expertise_options = ['Engineering', 'Human Resource', 'Finance', 'Education']

    unique_interviewer_names = set()  # To track unique names
    existing_interviewer_ids = set()
    # Assuming company_ids and cur have been defined earlier
    for company_id in company_ids:
        for field_expertise in field_expertise_options:
            # Generate a unique name for each interviewer
            while True:
                interviewer_name = faker.unique.name()
                if interviewer_name not in unique_interviewer_names:
                    unique_interviewer_names.add(interviewer_name)
                    break
            interviewer_id = generate_unique_interview_id(existing_interviewer_ids)
            existing_interviewer_ids.add(interviewer_id)  # Keep track of used IDs
            # Insert an interviewer for each field of expertise for the current company
            cur.execute("""
            INSERT INTO Interviewer (InterviewId, companyId, interviewerName, fieldExpertise) 
            VALUES (%s, %s, %s, %s)
            """, (interviewer_id,company_id, interviewer_name, field_expertise))

    # Fetch all interviewing applications
    cur.execute("SELECT applicationId, jobId FROM Applications WHERE currentStatus = 'Applied' AND isShortlisted = TRUE")
    interviewing_applications = cur.fetchall()

    for application_id, job_id in interviewing_applications:
        # Fetch the applicant's legal name
        cur.execute("""
        SELECT legalName FROM Applicant 
        WHERE email = (
            SELECT email FROM Applications WHERE applicationId = %s
        )
        """, (application_id,))

        # Fetch the required field of expertise and company ID for the job
        cur.execute("""
        SELECT  fieldId, companyId FROM Jobs WHERE jobId = %s
        """, (job_id,))
        required_field, company_id = cur.fetchone()
        d = {
            1:'Engineering',2: 'Human Resource', 3:'Finance',4: 'Education'
        }
        # Fetch the interviewer ID and name based on the company ID and field of expertise
        cur.execute("""
        SELECT InterviewId FROM Interviewer 
        WHERE companyId = %s AND fieldExpertise = %s
        """, (company_id, d[required_field]))
        result = cur.fetchone()
        if result:
            interviewer_id = result
            isSelected = random.randint(0, 2)  # Randomly choose between 0, 1, and 2

            # Insert the data into the Interview table including applicantLegalName and interviewerName
            cur.execute("""
            INSERT INTO Interview (applicationId, interviewerId, isSelected) 
            VALUES (%s, %s, %s)
            """, (application_id, interviewer_id, isSelected))

            # Update the currentStatus in the Applications table based on isSelected value
            if isSelected == 0:
                new_status = 'Rejected'
            elif isSelected == 1:
                new_status = 'Interviewing'  # Or consider another status if needed since they were already interviewing
            elif isSelected == 2:
                new_status = 'Hired'

            cur.execute("""
            UPDATE Applications SET currentStatus = %s WHERE applicationId = %s
            """, (new_status, application_id))

    conn.commit()
    print("Data generation and insertion complete.")

# if __name__ == "__main__":
#     conn = connect_to_db()
#     print(conn)
#     if conn:
#         create_tables(conn)
#         generate_and_insert_data(conn, 5000, 40, 10, 2)


# delete cascade