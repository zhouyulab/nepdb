# NEPdb SVM

## Training the model
    tar -xzvf data.tar.gz #extract training data
    tar -xzvf abstracts.tar.gz fulltext.tar.gz
    python trainSVM.py  # Training SVM model

## Using the model
    python neoantigenAbsFilter.py  # Filtering by abstract
    python neoantigenTextFilter.py # Filtering by full text
 
