# typedpath

Use typed Python objects to represent files and directories.

If you have a project that reads or writes non-trivial structures of directories and files it can be
hard to keep track of which structure they should have. `typedpath` allow you to declare the
structure using Python objects, and access the data with object methods.

Example:
```python
import typedpath as tp


class Person(tp.StructDir):
    name: tp.TextFile
    config: tp.JSONFile


class Database(tp.StructDir):
    people: tp.DictDir[str, Person]


d = Database("database")
d.people["alice"].name.write("Alice")
d.people["alice"].config.write({"require_authentication": True})
d.people["bob"].name.write("Bob")
d.people["bob"].config.write({"require_authentication": False})
```

```bash
> tree database/
database/
└── people
    ├── alice
    │   ├── config.json
    │   └── name.txt
    └── bob
        ├── config.json
        └── name.txt
```


## Built-in classes

`typedpath` comes with a built-in collection of classes for representing directories and files, and
you can create your own to support any additional types you need.



### `TextFile` and `BytesFile`

The two most basic classes included in `typedpath` are `TextFile` and `BytesFile`, which allows you
to read and write basic `str`s and `bytes`s. Both come with `read` and `write` methods for accessing
data:

```python
tf = tp.TextFile("my_text.txt")
tf.write("Hello, world!")
print(tf.read())

bf = tp.BytesFile("my_bytes.bin")
bf.write(b"Hello, world!")
print(bf.read())
```


### `StructDir` and passing arguments

The first class provided for composition is `StructDir`. A `StructDir` has a fixed number of
members that may have different types. The members are declared using Python type hints:

```python
class Person(tp.StructDir):
    name: tp.TextFile
    config: tp.JSONFile


class Database(tp.StructDir):
    people: tp.DictDir[str, Person]
```

All members should be a subclass of `tp.TypedPath`, and the name of the member becomes the name of
the file on the filesystem.

Some members may require configuration that is not (easily) expressible in the type system. For
example `TextFile` can take an `encoding` argument. To pass such arguments to the members you can
use the `withargs` function:

```python
class Person(tp.StructDir):
    name: tp.TextFile = tp.withargs(encoding="ascii")
    config: tp.JSONFile


p = Person("person")
p.name.write("Eve")
```


### `DictDir` and key encoding

The other class provided for composition is `DictDir`. The `DictDir` has a variable number of
members, but they must all have the same type. As the name implies the `DictDir` mimics a Python
`dict`, mapping filenames to `typedpath` objects.

If a `DictDir` is created as part of a `StructDir` the types of the keys and values are determined
from the type annotations in the `StructDir`. If you create a free-standing `DictDir` you must pass
the type of the keys and values to `__init__`:

```python
people = tp.DictDir("people", str, Person)
```

You can use the `value_args` keyword-argument to pass arguments to the children:

```python
configs = tp.DictDir("configs", str, tp.TextFile, value_args=tp.withargs(encoding="ascii"))
```

By default `DictDir` uses `str` to convert the keys into a filename, and the key types `__init__` to
convert filenames back into key objects. If that does not work for the type you would like to use
for keys, you can implement a `KeyCodec` for converting between your keys and strings:

```python
from typing import Type

class BoolKeyCodec(tp.KeyCodec[bool]):
    def encode(self, key: bool) -> str:
        return "True" if key else "False"

    def decode(self, key_str: str, key_type: Type[bool]) -> bool:
        assert issubclass(key_type, bool), key_type
        match key_str:
            case "True":
                return True
            case "False":
                return False
        raise AssertionError(f"Don't know how to interpret {key_str} as a bool")
```

Then register your codec for default use in all `DictDir`s:

```python
tp.add_key_codec(bool, BoolKeyCodec())
```

Or you can set which `KeyCodec` to use in just one specific `DictDir`:

```python
bools = tp.DictDir("bools", bool, tp.TextFile, key_codec=BoolKeyCodec())
```


### JSON support

`typedpath` provides `JSONFile` for reading and writing using Python's built-in `json` module:

```python
json = tp.JSONFile("example.json")
json.write(
    {
        "is_example": True,
        "example_names": ["alice", "bob", "eve"],
    }
)
print(json.read())
```


### Pickle support

For pickling objects `typedpath` provides the `PickleFile` class. It takes a parameter for which
type of object to (de)serialize:

```python
class A:
    def __init__(self, value: int) -> None:
        self.value = value

    def talk(self) -> None:
        print(self.value)

pf = tp.PickleFile("a.pickle", A)
pf.write(A(13))
pf.read().talk()
```

If used with a `StructDir` the type hint defines the kind of object to (de)serialize:

```python
class MyDir(tp.StructDir):
    a: tp.PickleFile[A]
    b: tp.TextFile


md = MyDir("my_dir")
md.a.write(A(42))
md.a.read().talk()
```


### NumPy support

`typedpath` also provides (admittedly limited) classes for reading and writing NumPy
arrays. `NpyFile` allows you to store a single array in a single file, and `NpzFile` does the same,
but with compression:

```python
import numpy as np

npy = tp.NpyFile("array.npy")
npy.write(np.array([1, 2, 3]))
print(npy.read())

npz = tp.NpzFile("array.npz")
npz.write(np.array([1, 2, 3]))
print(npz.read())
```


### Pandas support

`typedpath` has a couple of classes for reading and writing Pandas data frames, supporting `.csv`,
`.feather` and `.parquet` files:

```python
import pandas as pd

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
```


## Declaring your own classes

Obviously `typeddict` only provides a very small subset of the file types you may want to read and
write. It is expected you will need to write you own classes to support further file types. To
integrate with the `typedpath` framework your classes must:

1. If it is a file it should extend `tp.TypedFile`. If it is a directory it should extend
`tp.TypedDir`.

1. You class should have a static member variable called `default_suffix` defining
what the suffix of these objects normally is. It can be empty (`""`).

1. In simple cases do not define `__init__`. If you need to define `__init__` it must have: `self`; the filesystem path this object represents, with type `tp.PathLikeLike`; then any generic type arguments this class may need; and finally any keyword arguments your class needs for configuration.

1. To write to a file use `self.write_path()` to access the path. This method ensures any parent directories are created.

1. To read from a file use `self.read_path()` to access the path. This method ensures the path already exists.

1. To do anything else with the path, use `self.pretty_path()`.

1. Other than that, add any methods you feel you need to read/write data.

Generally the template is:

```python
class <YourClassName>(TypedFile):
    default_suffix = "<your suffix>"

    def __init__(
        self,
        path: PathLikeLike,
        <any generic type arguments go here>,
        *,
        <kwargs for configuration>
    ) -> None:
        super().__init__(path)

        <initialize stuff here>

    def write(self, ...) -> None:
        <write to self.write_path() here>

    def read(self) -> ...:
        <read from self.read_path() here>
```

For example, here's the implementation of `TextFile`:

```python
class TextFile(TypedFile):
    default_suffix = ".txt"

    def __init__(self, path: PathLikeLike, *, encoding: str = "utf-8") -> None:
        super().__init__(path)

        self._encoding = encoding

    def write(
        self,
        data: str,
        *,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        return self.write_path().write_text(
            data, encoding=self._encoding, errors=errors, newline=newline
        )

    def read(self, errors: str | None = None) -> str:
        return self.read_path().read_text(encoding=self._encoding, errors=errors)
```

And `PickleFile` (which is a generic class):

```python
class PickleFile(TypedFile, Generic[T]):
    default_suffix = ".pickle"

    def __init__(self, path: PathLikeLike, value_type: Type[T]) -> None:
        super().__init__(path)

        self._value_type = value_type

    def write(self, data: T, **kwargs: Any) -> None:
        with open(self.write_path(), "wb") as fp:
            pickle.dump(data, fp, **kwargs)

    def read(self, **kwargs: Any) -> T:
        with open(self.read_path(), "rb") as fp:
            result: T = pickle.load(fp, **kwargs)
            origin = get_origin(self._value_type)
            if origin is not None:
                assert isinstance(result, origin)
            return result
```