import sys
from pathlib import Path
sys.path.insert(0, str(Path('/home/res/Research/230957020/sentiment_impact_trading/src')))

import impact_scorer as isc

result = isc.run_pipeline('RBI hikes repo rate by 25 bps')
print("Pipeline result:")
print(result)
