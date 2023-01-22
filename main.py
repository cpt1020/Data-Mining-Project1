from pathlib import Path
from typing import List
import src.utils as utils
import src.config as config
import src.args as args
from src.apriori import *
from src.fp_growth import fp_growth

def main():
    # Parse command line arguments
    a = args.parse_args()

    # Load dataset, the below io handles ibm dataset
    input_data: List[List[str]] = utils.read_file(config.IN_DIR / a.dataset)
    filename = Path(a.dataset).stem

    print("\nApriori--------------------------------------------")
    apriori_out = apriori(input_data, a.min_sup, a.min_conf)

    # write apriori result to .csv
    utils.write_file(
        data=apriori_out,
        filename=config.OUT_DIR / f"{filename}-apriori (min_sup {a.min_sup}, min_conf {a.min_conf}).csv"
    )

    print("\nFP Growth--------------------------------------------")
    fp_growth_out = fp_growth(input_data, a.min_sup, a.min_conf)
    
    # write fp-growth result to .csv
    utils.write_file(
        data=fp_growth_out,
        filename=config.OUT_DIR / f"{filename}-fp_growth (min_sup {a.min_sup}, min_conf {a.min_conf}).csv"
    )

if __name__ == "__main__":
    main()