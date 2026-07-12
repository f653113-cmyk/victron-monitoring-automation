"""
Dashboard Generator
Creates beautiful Tableau/Power BI level visualizations
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardGenerator:
    def __init__(self):
        self.html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .header p {{
            color: #666;
            font-size: 1.1em;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }}
        .card.critical {{
            border-left-color: #e74c3c;
        }}
        .card.warning {{
            border-left-color: #f39c12;
        }}
        .card.success {{
            border-left-color: #27ae60;
        }}
        .card h3 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .card.critical .value {{
            color: #e74c3c;
        }}
        .card.warning .value {{
            color: #f39c12;
        }}
        .card.success .value {{
            color: #27ae60;
        }}
        .card .unit {{
            font-size: 0.5em;
            color: #999;
        }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .chart-container h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        .sites-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .site-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .site-card h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        .site-metric {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .site-metric label {{
            color: #666;
            font-weight: 500;
        }}
        .site-metric value {{
            color: #333;
            font-weight: bold;
        }}
        .anomalies {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .anomalies h2 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .anomaly-item {{
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border-left: 5px solid #999;
        }}
        .anomaly-item.critical {{
            background: #fadbd8;
            border-left-color: #e74c3c;
        }}
        .anomaly-item.warning {{
            background: #fef5e7;
            border-left-color: #f39c12;
        }}
        .anomaly-type {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .anomaly-message {{
            color: #333;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Solar Monitoring Dashboard</h1>
            <p>Powered by Victron VRM | Generated: {timestamp}</p>
        </div>

        <!-- Summary Cards -->
        <div class="grid">
            {summary_cards}
        </div>

        <!-- Sites Performance -->
        <div class="sites-grid">
            {site_cards}
        </div>

        <!-- Anomalies -->
        {anomalies_section}

        <div class="footer">
            <p>Automated Solar Monitoring System | All times in UTC</p>
        </div>
    </div>

    <script>
        // Charts will be rendered here
        {charts_js}
    </script>
</body>
</html>
        """

    def generate_dashboard(self, analysis_data):
        """Generate HTML dashboard"""
        logger.info("Generating dashboard...")

        summary = analysis_data.get('summary', {})
        sites = analysis_data.get('sites', [])
        anomalies = analysis_data.get('anomalies', [])

        # Generate cards
        summary_cards = self._generate_summary_cards(summary, anomalies)
        site_cards = self._generate_site_cards(sites)
        anomalies_section = self._generate_anomalies_section(anomalies)

        # Generate HTML
        html = self.html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            summary_cards=summary_cards,
            site_cards=site_cards,
            anomalies_section=anomalies_section,
            charts_js=""
        )

        # Save
        Path('reports').mkdir(exist_ok=True)
        dashboard_path = 'reports/dashboard.html'
        with open(dashboard_path, 'w') as f:
            f.write(html)

        logger.info(f"Dashboard saved to {dashboard_path}")
        return dashboard_path

    def _generate_summary_cards(self, summary, anomalies):
        """Generate summary KPI cards"""
        html = ""

        # Total Production
        html += f"""
        <div class="card success">
            <h3>Total Production</h3>
            <div class="value">{summary.get('total_production_kwh', 0):.1f}<span class="unit">kWh</span></div>
        </div>
        """

        # Average Efficiency
        eff = summary.get('avg_efficiency_pct', 0)
        card_class = "card critical" if eff < 75 else "card warning" if eff < 85 else "card success"
        html += f"""
        <div class="{card_class}">
            <h3>Avg Efficiency</h3>
            <div class="value">{eff:.1f}<span class="unit">%</span></div>
        </div>
        """

        # Battery SOC
        soc = summary.get('avg_battery_soc_pct', 0)
        card_class = "card critical" if soc < 20 else "card warning" if soc < 50 else "card success"
        html += f"""
        <div class="{card_class}">
            <h3>Avg Battery SOC</h3>
            <div class="value">{soc:.1f}<span class="unit">%</span></div>
        </div>
        """

        # Active Sites
        html += f"""
        <div class="card success">
            <h3>Active Sites</h3>
            <div class="value">{summary.get('total_sites', 0)}</div>
        </div>
        """

        # Anomalies
        anomaly_count = len(anomalies)
        card_class = "card critical" if anomaly_count > 0 else "card success"
        html += f"""
        <div class="{card_class}">
            <h3>Anomalies Detected</h3>
            <div class="value">{anomaly_count}</div>
        </div>
        """

        return html

    def _generate_site_cards(self, sites):
        """Generate individual site cards"""
        html = ""

        for site in sites:
            name = site.get('name', 'Unknown')
            kpis = site.get('kpis', {})

            html += f"""
            <div class="site-card">
                <h3>{name}</h3>
                <div class="site-metric">
                    <label>Production:</label>
                    <value>{kpis.get('total_production_kwh', 0):.2f} kWh</value>
                </div>
                <div class="site-metric">
                    <label>Efficiency:</label>
                    <value>{kpis.get('avg_efficiency_pct', 0):.1f}%</value>
                </div>
                <div class="site-metric">
                    <label>Peak Power:</label>
                    <value>{kpis.get('peak_power_w', 0):.0f} W</value>
                </div>
                <div class="site-metric">
                    <label>Avg Load:</label>
                    <value>{kpis.get('avg_load_pct', 0):.1f}%</value>
                </div>
                <div class="site-metric">
                    <label>Battery SOC:</label>
                    <value>{kpis.get('avg_battery_soc_pct', 0):.1f}%</value>
                </div>
                <div class="site-metric">
                    <label>Min Battery:</label>
                    <value>{kpis.get('min_battery_soc_pct', 0):.1f}%</value>
                </div>
            </div>
            """

        return html

    def _generate_anomalies_section(self, anomalies):
        """Generate anomalies section"""
        if not anomalies:
            return '<div class="anomalies"><h2>✅ No Anomalies Detected</h2></div>'

        html = '<div class="anomalies"><h2>⚠️ Detected Issues</h2>'

        for anomaly in anomalies:
            severity = anomaly.get('severity', 'WARNING').lower()
            html += f"""
            <div class="anomaly-item {severity}">
                <div class="anomaly-type">{anomaly.get('type', 'UNKNOWN')}</div>
                <div class="anomaly-message">{anomaly.get('message', 'N/A')}</div>
            </div>
            """

        html += '</div>'
        return html

def main(analysis_file='data/analysis.json'):
    """Main execution"""
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)

    generator = DashboardGenerator()
    dashboard_path = generator.generate_dashboard(analysis)
    return dashboard_path

if __name__ == "__main__":
    main()
