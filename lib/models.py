import pandas
import ast
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR
from sklearn.svm import NuSVR
from sklearn.svm import SVR


def __load_file(file, stat_verbose=False):
    emotional_data = pandas.read_csv(file, sep=",", names=["lp", "bpm", "valence", "arousal"], skiprows=1)

    result = []
    x = []
    y = []

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
                if percent_done >= 2:
                    break
                print(f"{percent_done}% done")

    print("First loop done")
    for i in result:
        x.append([i[0], i[1]])
        #y.append([i[1], i[2]])
        y.append(i[2])

    print("Second loop done")

    return x, y


def __create_tuples(bpm, gsr, valence, arousal):
    result = []
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

    return result


def __is_gsr_valid(gsr) -> bool:
    for i in gsr:
        if i != 0.0:
            return True

    return False

def __get_models():
    models = []

    # Ordinary least squares Linear Regression
    #models.append(('LR', LogisticRegression()))

    # Nu Support Vector Regression
    #models.append(('NuSVR', NuSVR()))

    # Epsilon-Support Vector Regression
    models.append(('SVR', SVR()))

    # Linear Support Vector Regression
    models.append(('LinearSVR', LinearSVR()))

    # Multi-layer Perceptron regressor
    models.append(('MLPRegressor', MLPRegressor()))

    return models


def validate_models(file):
    (x, y) = __load_file(file, stat_verbose=True)

    validation_size = 0.15
    seed = 7

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
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
