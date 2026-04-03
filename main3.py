import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, request, jsonify
from sqlalchemy import create_engine

app = Flask(__name__)

# Postgres Connection - Update with your credentials
DB_URL = "postgresql://postgres:password@localhost:5432/customer_service_db"
engine = create_engine(DB_URL)

def get_base64_image():
    """Converts the current matplotlib plot to a base64 string for React."""
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    return encoded_img

@app.route('/api/visualize/dynamic', methods=['GET'])
def visualize_any_data():
    """
    Query Params:
    - table: The DB table name (e.g., 'complaints', 'requests', 'users')
    - x_axis: The column to plot on X (e.g., 'status', 'priority', 'category')
    - hue: (Optional) The column for color grouping (e.g., 'priority')
    """
    table_name = request.args.get('table')
    x_col = request.args.get('x_axis')
    hue_col = request.args.get('hue', None)

    if not table_name or not x_col:
        return jsonify({"error": "Missing 'table' or 'x_axis' parameters"}), 400

    try:
        # 1. Fetch data dynamically
        # Using a formatted string for table name (ensure your Java backend validates the table name)
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql(query, engine)

        if df.empty:
            return jsonify({"error": f"No data found in {table_name}"}), 404

        # 2. Setup Plotting
        plt.figure(figsize=(12, 7))
        sns.set_style("darkgrid")
        
        # Determine plot type: Countplot is best for categorical Customer Service data
        sns.countplot(data=df, x=x_col, hue=hue_col, palette="magma")
        
        plt.title(f"Analysis of {table_name.capitalize()} by {x_col.capitalize()}")
        plt.xticks(rotation=45)

        # 3. Return JSON with image and basic stats
        return jsonify({
            "image": get_base64_image(),
            "total_records": len(df),
            "columns": list(df.columns)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
