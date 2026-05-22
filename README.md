# polar-tides
`polar-tides` is a Python library to assist in enforcing/validating `[polars](https://pola.rs/)` dataframes against the [TIDES](https://github.com/TIDES-transit/TIDES) data standards using [dataframely](https://github.com/Quantco/dataframely) schema objects.  

This library is in alpha andnot yet intended for production use. It is undergoing active development, so expect breaking changes.  


## Use

```python

import dataframely as dy
import polars as pl
import polartides as tides


def create_trips_performed() -> tides.TripsPerformed:  # Use dataframely schemas as return-types
    """
    Agency-specific code that returns a TIDES:trips_performed-compliant polars dataframe.
    
    Raises dataframely.exc.SchemaError
    """
    df: pl.DataFrame = ...  # create the dataframe
    return tides.TripsPerformed.validate(df)  # Returns a TIDES schema-validated polars dataframe

```

## Installation (WIP)
_This is not yet available on pypi_

Download this repo and copy the `polartides` folder to your PATH.  


## Contributing
Please!  
We need tests and sample data.  
