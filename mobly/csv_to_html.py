import pandas as pd
import gTAF_config

df = pd.read_csv(gTAF_config.execution_summary_csv_file)
df.to_html(gTAF_config.html_report_file)
htmTable = df.to_html()

