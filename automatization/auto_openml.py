from get_dataset import *
from get_statistic_summary import *
from get_mljar import *


def main():
    id = input('Please enter the dataset id:')
    id = str(id)
    catalog = latest_catalog()
    data = load_dataset(id, catalog)
    print("Successfully uploaded dataset.")
    profiling = generate_pandas_profiling(id, data)
    get_statistic_summary(id, profiling)
    print("Successfully generated Pandas Profiling.")
    target = input('Please enter the name of the target variable:')
    target = str(target)
    task = input('Please enter the chosen ML task (regression/binary_classification/multi_classification):')
    prep_data = prepare_to_mljar(data=data,target_variable=target, task=task, profiling=profiling)
    generate_mljar(data = prep_data, target_variable=target)
    print("Successfully generated AutoML report.")


if __name__ == "__main__":
    main()
