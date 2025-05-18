from flask import Flask
import pymysql
from pymysql import Error

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="kannan_45",
    charset="utf8",
    database="chain_of_custody"
)

app = Flask(__name__)

@app.route('/test-db')
def test_db_connection():
    try:
        if mydb.open:
            return "Database connection successful!"
    except Error as e:
        return f"Error connecting to the database: {e}"

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)
