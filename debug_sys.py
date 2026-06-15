import traceback

print("Trying to import pandas...")
try:
    import pandas
    print("pandas imported successfully")
except Exception as e:
    traceback.print_exc()

print("\nTrying to import numpy...")
try:
    import numpy
    print("numpy imported successfully")
except Exception as e:
    traceback.print_exc()

print("\nTrying to import sklearn...")
try:
    import sklearn
    print("sklearn imported successfully")
except Exception as e:
    traceback.print_exc()

print("\nTrying to import narwhals...")
try:
    import narwhals
    print("narwhals imported successfully")
except Exception as e:
    traceback.print_exc()

print("\nTesting narwhals from_native...")
try:
    import narwhals as nw
    import pandas as pd
    df = pd.DataFrame({'a': [1]})
    nw.from_native(df)
    print("narwhals from_native completed successfully")
except Exception as e:
    traceback.print_exc()
