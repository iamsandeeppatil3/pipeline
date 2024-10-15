from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'sandeep',
    'password': 'Pass@123',
    'host': 'localhost',
    'database': 'library'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        table_name = request.form['table']
        data = request.form['data']
        # Assuming the data input is simple and matches the column structure
        columns = data.split(',')
        
        # Adjust this according to your table structure
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f'INSERT INTO {table_name} VALUES ({placeholders})'
        cursor.execute(sql, columns)
        conn.commit()
        return redirect(url_for('index'))

    # Fetch all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Fetch data for each table
    table_data = {}
    for (table_name,) in tables:
        cursor.execute(f'SELECT * FROM {table_name}')
        table_data[table_name] = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('index.html', tables=tables, table_data=table_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

