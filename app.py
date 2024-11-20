from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import os
from create_table import *

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', "dbname='ATSDUMMY1' user='postgres' host='localhost' password='Chirayu@123'")
#DATABASE_URL = os.environ.get('DATABASE_URL', "postgres://admin:n7BVjW83CNT1m9n89UuCPgWrDdBFjfBI@dpg-conbiscf7o1s73fh9q20-a.oregon-postgres.render.com/ats")


def execute_query(query):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        results = cur.fetchall()
        return results
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    
@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("select * from fields;")
    except Exception as e:
        print(conn)
        if conn:
            create_tables(conn)
            generate_and_insert_data(conn, 5000, 40, 10, 2)
    finally:
        cur.close()
        conn.close()
    
        
    return render_template('index.html')

@app.route('/execute_query', methods=['POST'])
def execute():
    query_number = request.form['query_number']
    
    queries = {
        "1": "SELECT * FROM jobs ORDER BY postedDate DESC;",
        # Add other predefined queries as mapped WHERE current_date - postedDate <= 10
        "2": '''
            SELECT a.email, c.companyName, i.interviewerId, i.isSelected
            FROM Interview i
            JOIN Applications ap ON i.applicationId = ap.applicationId
            JOIN Applicant a ON ap.email = a.email
            JOIN Companies c ON c.companyId = (SELECT companyId FROM Jobs WHERE jobId = ap.jobId)
            ORDER BY i.interviewerId ASC;  -- Assuming interviewId is scheduled in ascending order
''',
        "3": '''SELECT j.*
            FROM Jobs j
            JOIN Fields f ON j.fieldId = f.fieldId
            WHERE j.isActive = TRUE AND j.requiredWorkSetting = 'Onsite' AND f.fieldName = 'Finance';''',
        "4": '''SELECT 
            A.email,
            A.legalName,
            A.skills,
            A.yearOfExperience,
            A.workSetting,
            COUNT(AP.applicationId) AS NumberOfApplications,
            MAX(J.postedDate) AS MostRecentApplicationDate,
            LATEST_APP.jobTitle AS LatestJobTitle,
            LATEST_APP.jobDescription AS LatestJobDescription
        FROM 
            Applicant A
        INNER JOIN 
            Applications AP ON A.email = AP.email
        INNER JOIN 
            Jobs J ON AP.jobId = J.jobId
        LEFT JOIN 
            Jobs LATEST_APP ON LATEST_APP.jobId = (
                SELECT jobId FROM Applications 
                WHERE email = A.email 
                ORDER BY applicationId DESC LIMIT 1
            )
        WHERE 
            J.isActive = TRUE
        GROUP BY 
            A.email, A.legalName, A.skills, A.yearOfExperience, A.workSetting, LATEST_APP.jobTitle, LATEST_APP.jobDescription
        ORDER BY 
            NumberOfApplications DESC, MostRecentApplicationDate DESC
        LIMIT 5;
''',
        "5":'''SELECT 
                C.companyName,
                COUNT(A.applicationId) AS NumberOfApplications
            FROM 
                Companies C
            JOIN 
                Jobs J ON C.companyId = J.companyId
            JOIN 
                Applications A ON J.jobId = A.jobId
            JOIN 
                Fields F ON J.fieldId = F.fieldId
            WHERE 
                F.fieldName = 'Finance'
            GROUP BY 
                C.companyName
            ORDER BY 
                NumberOfApplications DESC;
''',
        "6": '''SELECT 
    A.legalName AS ApplicantName,
    A.email AS ApplicantEmail,
    I.interviewerName AS InterviewerName,
    AP.isShortlisted AS Shortlisted
FROM 
    Applications AP
JOIN 
    Applicant A ON AP.email = A.email
JOIN 
    Interview INTR ON AP.applicationId = INTR.applicationId
JOIN 
    Interviewer I ON INTR.interviewerId = I.InterviewId
WHERE 
    AP.isShortlisted = TRUE
ORDER BY 
    A.legalName;
''',
    }
    executed_query = queries[query_number]
    results = execute_query(queries[query_number])
    
    return render_template('results.html', rows=results, executed_query=executed_query)

@app.route('/query', methods=['POST'])
def query():
    sql = request.form['sql']
    results = execute_query(sql)
    return render_template('results.html', rows=results)

if __name__ == '__main__':
    app.run(debug=True)
