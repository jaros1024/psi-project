import pandas
import ast
from sklearn import model_selection
from pathlib import Path


from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier


import numpy as np
import lib.emotions as emotions

FINAL_DATA_FILE = "final.csv"
PROCESSED_DATA_FILE = "processed.csv"


def __load_file(stat_verbose=False):
    tuple_file = Path(FINAL_DATA_FILE)
    if tuple_file.exists():
        result = __load_tuples(FINAL_DATA_FILE)
    else:
        result = __make_tuples(PROCESSED_DATA_FILE, stat_verbose=stat_verbose)

    x = []
    y = []

    for i in result:
        x.append([i[0], i[1]])
        y.append(emotions.emotion_data_to_class(i[2], i[3]))

    print("Second loop done")
    print(f"Number of examples: {len(x)}")

    return x, y


def __create_tuples(bpm, gsr, valence, arousal):
    result = []
    if len(bpm) == 0:
        return result

    per_bpm = int(round(len(gsr) / len(bpm)))

    bpm_ptr = 0
    counter = 0
    for i in gsr:
        try:
            result.append([bpm[bpm_ptr], i, valence, arousal])
            counter += 1
            if counter == per_bpm:
                bpm_ptr += 1
                counter = 0
        except IndexError:
            break

    return __mean_tuples(result)


def __mean_tuples(values: []) -> []:
    result = []
    gsr = []
    current_bpm = values[0][0]

    for i in values:
        if i[0] != current_bpm:
            if len(gsr) == 0:
                result.append((i[0], i[1], i[2], i[3]))
            else:
                result.append((current_bpm, np.mean(gsr), i[2], i[3]))
                gsr = []
            current_bpm = i[0]
        else:
            gsr.append(i[1])

    return result


def __save_tuples(tuples: [], file: str):
    pandas.DataFrame(tuples).to_csv(file, sep=",", index=False)


def __load_tuples(file: str):
    data = pandas.read_csv(file, sep=",")
    return data.values


def __make_tuples(file: str, stat_verbose=False) -> []:
    emotional_data = pandas.read_csv(file, sep=",", names=["lp", "bpm", "valence", "arousal"], skiprows=1)

    result = []

    if stat_verbose:
        percent_done = 0
        rows_done = 0
        total_rows = len(emotional_data.values)

    for i in emotional_data.values:
        bpm = ast.literal_eval(i[0])
        gsr = ast.literal_eval(i[1])
        if __is_gsr_valid(gsr):
            result.extend(__create_tuples(bpm, gsr, i[2], i[3]))

        if stat_verbose:
            rows_done = rows_done + 1
            new_percent_done = int(round((rows_done / total_rows) * 100))
            if new_percent_done > percent_done:
                percent_done = new_percent_done
                # if percent_done >= 60:
                #     break
                print(f"{percent_done}% done")

    __save_tuples(result, "final.csv")
    return result


def __is_gsr_valid(gsr) -> bool:
    for i in gsr:
        if i != 0.0:
            return True

    return False


def __get_models():
    models = []

    # models.append(('Linear SVM', SVC(kernel="linear", C=0.025)))
    #
    # models.append(('RBF SVM', SVC(gamma=2, C=1)))
    #
    #models.append(('Decision Tree', DecisionTreeClassifier(max_depth=5,min_samples_split=0.012,min_samples_leaf=0.001)))
    #
    # models.append(('Random Forest', RandomForestClassifier(max_depth=8, n_estimators=100, max_features='auto',min_samples_split =3)))
    #
    # models.append(('Neural Net', MLPClassifier(hidden_layer_sizes=(4,20,10,5))))
    #
    # models.append(('AdaBoost', AdaBoostClassifier(n_estimators=300)))
    #
    # models.append(('Naive Bayes', GaussianNB()))
    #
    # models.append(('Bagging',BaggingClassifier(base_estimator=None, n_estimators=10, max_samples=1.0, max_features=1.0, bootstrap=True, bootstrap_features=False, oob_score=False, warm_start=False, n_jobs=1, random_state=None, verbose=0)))
    #
    # models.append(('ExtraTree',ExtraTreesClassifier()))
    #
    #models.append(('GradientBoosting', GradientBoostingClassifier(max_depth=6,min_samples_split=0.0001)))
    #
    #models.append(('Decision Tree', DecisionTreeClassifier(max_depth=6, criterion="entropy", min_samples_split=30))) JARKA

    return models


def __choose_best_model(names: [], results: []):
    max = -float("inf")
    ptr = -1
    for i in range(len(names)):
        if results[i].mean() > max:
            ptr = i
            max = results[i].mean()
    return names[ptr]


def validate_models(validation_size, seed):
    (x, y) = __load_file(stat_verbose=True)



    print("Creating training and validation lists")
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x, y, test_size=validation_size,
                                                                                    random_state=seed)
    models = __get_models()

    results = []
    names = []
    for name, model in models:
        print(f"Validating model {name}")
        kfold = model_selection.KFold(n_splits=10, random_state=seed)

        cv_results = model_selection.cross_val_score(model, x_train, y_train, cv=kfold, scoring="accuracy")
        results.append(cv_results)
        names.append((name, model))
        msg = "%s: mean: %f , std: %f" % (name, cv_results.mean(), cv_results.std())
        print(msg)

    name, model = __choose_best_model(names, results)
    print(f"Best model is {name}")

    model.fit(x_train, y_train)
    predictions = model.predict(x_validation)

    scored_value = accuracy_score(y_validation, predictions)
    print(f"Accuracy score is: {scored_value}")

    return scored_value
