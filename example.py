# from typing import Type

# import numpy as np

import pandas as pd

import typedpath as tp

# class Person(tp.StructDir):
#     name: tp.TextFile
#     config: tp.JSONFile
#
#
# class Database(tp.StructDir):
#     people: tp.DictDir[str, Person]
#
#
# d = Database("database")
# d.people["alice"].name.write("Alice")
# d.people["alice"].config.write({"require_authentication": True})
# d.people["bob"].name.write("Bob")
# d.people["bob"].config.write({"require_authentication": False})
#
#
# tf = tp.TextFile("my_text.txt")
# tf.write("Hello, world!")
# print(tf.read())
#
# bf = tp.BytesFile("my_bytes.bin")
# bf.write(b"Hello, world!")
# print(bf.read())
#
#
# class Person(tp.StructDir):
#     name: tp.TextFile = tp.withargs(encoding="ascii")
#     config: tp.JSONFile
#
#
# p = Person("person")
# p.name.write("Eve")
#
# people = tp.DictDir("people", str, Person)
# people["eve"].name.write("Eve")
#
# configs = tp.DictDir("configs", str, tp.TextFile, value_args=tp.withargs(encoding="ascii"))
# configs["json"].write("test")
#
#
# class BoolKeyCodec(tp.KeyCodec[bool]):
#     def encode(self, key: bool) -> str:
#         return "True" if key else "False"
#
#     def decode(self, key_str: str, key_type: Type[bool]) -> bool:
#         assert issubclass(key_type, bool), key_type
#         match key_str:
#             case "True":
#                 return True
#             case "False":
#                 return False
#         raise AssertionError(f"Don't know how to interpret {key_str} as a bool")
#
#
# bools = tp.DictDir("bools", bool, tp.TextFile, key_codec=BoolKeyCodec())
#
# tp.add_key_codec(bool, BoolKeyCodec())
#
# json = tp.JSONFile("example.json")
# json.write(
#     {
#         "is_example": True,
#         "example_names": ["alice", "bob", "eve"],
#     }
# )
# print(json.read())
#
#
# class A:
#     def __init__(self, value: int) -> None:
#         self.value = value
#
#     def talk(self) -> None:
#         print(self.value)
#
#
# class MyDir(tp.StructDir):
#     a: tp.PickleFile[A]
#     b: tp.TextFile
#
#
# md = MyDir("my_dir")
# md.a.write(A(42))
# md.a.read().talk()
#
# pf = tp.PickleFile("a.pickle", A)
# pf.write(A(13))
# pf.read().talk()
#
#
# npy = tp.NpyFile("array.npy")
# npy.write(np.array([1, 2, 3]))
# print(npy.read())
#
# npz = tp.NpzFile("array.npz")
# npz.write(np.array([1, 2, 3]))
# print(npz.read())


df = pd.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [True, False, True],
    }
)

csv = tp.PandasCsvFile("df.csv")
csv.write(df)
print(csv.read())

feather = tp.PandasFeatherFile("df.feather")
feather.write(df)
print(feather.read())

parquet = tp.PandasParquetFile("df.parquet")
parquet.write(df)
print(parquet.read())
