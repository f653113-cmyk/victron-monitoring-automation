"""
Email Sender
Sends reports via Gmail SMTP
"""

import smtplib
import logging
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self, gmail_address, gmail_password):
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_report(self, recipients, subject, html_body, attachments=None):
        """Send email report"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_address
            msg['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients
            msg['Subject'] = subject

            # Add HTML body
            msg.attach(MIMEText(html_body, 'html'))

            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    if Path(attachment_path).exists():
                        self._attach_file(msg, attachment_path)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_password)
                server.send_message(msg)

            logger.info(f"Email sent to {recipients}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def _attach_file(self, msg, filepath):
        """Attach file to email"""
        try:
            attachment = open(filepath, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {Path(filepath).name}')
            msg.attach(part)
            attachment.close()
        except Exception as e:
            logger.error(f"Failed to attach {filepath}: {e}")

    def create_report_html(self, analysis_data, report_type='full'):
        """Create HTML email body"""
        summary = analysis_data.get('summary', {})
        sites = analysis_data.get('sites', [])
        anomalies = analysis_data.get('anomalies', [])

        if report_type == 'alert' and not anomalies:
            return None

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #667eea; }}
                h2 {{ color: #333; margin-top: 20px; }}
                .summary {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .kpi {{ display: inline-block; margin-right: 30px; }}
                .kpi-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                .kpi-label {{ color: #666; font-size: 12px; }}
                .site {{ background: white; border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .anomaly {{ background: #fee; padding: 15px; margin: 10px 0; border-left: 4px solid #e74c3c; }}
                .anomaly.warning {{ background: #fef5e7; border-left-color: #f39c12; }}
                .anomaly-type {{ font-weight: bold; margin-bottom: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #667eea; color: white; }}
                .footer {{ color: #999; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <h1>⚡ Solar Monitoring Report</h1>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>

            <div class="summary">
                <h2>Summary</h2>
                <div class="kpi">
                    <div class="kpi-label">Total Production</div>
                    <div class="kpi-value">{summary.get('total_production_kwh', 0):.1f} kWh</div>
                </div>
                <div class="kpi">
                    <div class="kpi-label">Avg Efficiency</div>
                    <div class="kpi-value">{summary.get('avg_efficiency_pct', 0):.1f}%</div>
                </div>
                <div class="kpi">
                    <div class="kpi-label">Avg Battery SOC</div>
                    <div class="kpi-value">{summary.get('avg_battery_soc_pct', 0):.1f}%</div>
                </div>
                <div class="kpi">
                    <div class="kpi-label">Active Sites</div>
                    <div class="kpi-value">{summary.get('total_sites', 0)}</div>
                </div>
            </div>

            <h2>Site Performance</h2>
            <table>
                <tr>
                    <th>Site</th>
                    <th>Production (kWh)</th>
                    <th>Efficiency (%)</th>
                    <th>Battery SOC (%)</th>
                    <th>Peak Power (W)</th>
                </tr>
        """

        for site in sites:
            kpis = site.get('kpis', {})
            html += f"""
                <tr>
                    <td>{site.get('name', 'Unknown')}</td>
                    <td>{kpis.get('total_production_kwh', 0):.2f}</td>
                    <td>{kpis.get('avg_efficiency_pct', 0):.1f}</td>
                    <td>{kpis.get('avg_battery_soc_pct', 0):.1f}</td>
                    <td>{kpis.get('peak_power_w', 0):.0f}</td>
                </tr>
            """

        html += """
            </table>
        """

        # Anomalies
        if anomalies:
            html += "<h2>⚠️ Anomalies Detected</h2>"
            for anomaly in anomalies:
                severity_class = 'warning' if anomaly.get('severity') == 'WARNING' else ''
                html += f"""
                <div class="anomaly {severity_class}">
                    <div class="anomaly-type">{anomaly.get('type', 'UNKNOWN')} ({anomaly.get('severity', 'WARNING')})</div>
                    <div>{anomaly.get('message', 'N/A')}</div>
                </div>
                """
        else:
            html += "<h2>✅ No Anomalies Detected</h2>"

        html += """
            <div class="footer">
                <p>This is an automated report from the Solar Monitoring System.</p>
                <p>For more details, visit your dashboard at: <a href="https://your-dashboard-url">Dashboard Link</a></p>
            </div>
        </body>
        </html>
        """

        return html

def main(analysis_file='data/analysis.json', gmail_user=None, gmail_pass=None, recipients=None):
    """Main execution"""
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)

    if not gmail_user or not gmail_pass or not recipients:
        logger.error("Missing Gmail credentials or recipients")
        return False

    sender = EmailSender(gmail_user, gmail_pass)
    html_body = sender.create_report_html(analysis)

    if html_body:
        return sender.send_report(
            recipients,
            f"Solar Monitoring Report - {datetime.now().strftime('%Y-%m-%d')}",
            html_body,
            attachments=['reports/dashboard.html']
        )

    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        print("Usage: python email_sender.py <analysis_file> <gmail_user> <gmail_pass> <recipient1> [recipient2...]")
