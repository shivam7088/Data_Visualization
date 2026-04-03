import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, request, jsonify
from sqlalchemy import create_engine

app = Flask(__name__)

# Replace with your actual Postgres credentials
# Format: postgresql://username:password@localhost:5432/your_database
DB_URL = "postgresql://postgres:password@localhost:5432/customer_service_db"
engine = create_engine(DB_URL)

def get_base64_image():
    """Converts the plot in memory to a base64 string."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img_str

@app.route('/api/visualize', methods=['GET'])
def visualize_data():
    category = request.args.get('category', 'complaints') # 'requests' or 'complaints'
    chart_type = request.args.get('type', 'status_count')

    try:
        # 1. Fetch data from your Postgres tables
        query = f"SELECT * FROM {category}"
        df = pd.read_sql(query, engine)

        if df.empty:
            return jsonify({"error": "No data found in table"}), 404

        # 2. Generate the Visualization
        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")

        if chart_type == 'status_count':
            # Visualizing how many complaints are 'Pending' vs 'Resolved'
            sns.countplot(data=df, x='status', palette='viridis')
            plt.title(f'Total {category.capitalize()} by Status')
        
        elif chart_type == 'priority_dist':
            # Visualizing priority levels (High, Medium, Low)
            sns.histplot(data=df, x='priority', hue='status', multiple='stack')
            plt.title(f'Priority Distribution of {category.capitalize()}')

        # 3. Return the image string
        return jsonify({
            "image": get_base64_image(),
            "summary": df.describe(include='all').to_dict()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Running on port 5001 so it doesn't conflict with your Java (8080) or React (3000)
    app.run(port=5001, debug=True)